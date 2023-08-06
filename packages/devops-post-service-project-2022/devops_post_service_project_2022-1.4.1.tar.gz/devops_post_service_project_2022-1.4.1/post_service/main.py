from fastapi import FastAPI, Body, Request, Query, File
from fastapi.responses import FileResponse
from fastapi_contrib.conf import settings
from fastapi.encoders import jsonable_encoder
from kafka import KafkaProducer
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId, json_util
import uvicorn
from pymongo import MongoClient
import jwt
from jaeger_client import Config
from opentracing.scope_managers.asyncio import AsyncioScopeManager
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info
import os
import json
import time
import uuid
import shutil


POSTS_URL = '/api/posts'
COMMENTS_URL = '/api/comments'

DB_USERNAME = os.getenv('DB_USERNAME', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_CONTAINER_NAME = os.getenv('DB_CONTAINER_NAME', 'post_container')
DB_PORT = os.getenv('DB_PORT', '27017')
DB_NAME = os.getenv('DB_NAME', 'post')

KAFKA_HOST = os.getenv('KAFKA_HOST', 'kafka')
KAFKA_PORT = os.getenv('KAFKA_PORT', '9092')
KAFKA_EVENTS_TOPIC = os.getenv('KAFKA_EVENTS_TOPIC', 'events')
KAFKA_NOTIFICATIONS_TOPIC = os.getenv('KAFKA_NOTIFICATIONS_TOPIC', 'notifications')
JWT_SECRET = os.getenv('JWT_SECRET', 'jwt_secret')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')


app = FastAPI(title='Post Service API')
client = MongoClient(f'mongodb://{DB_CONTAINER_NAME}:{DB_PORT}/{DB_NAME}?authSource=admin', username=DB_USERNAME, password=DB_PASSWORD)
db = client.post
post_col = db.post
comment_col = db.comment
like_col = db.like
dislike_col = db.dislike
kafka_producer = None

def setup_opentracing(app):
    config = Config(
        config={
            "local_agent": {
                "reporting_host": settings.jaeger_host,
                "reporting_port": settings.jaeger_port
            },
            "sampler": {
                "type": settings.jaeger_sampler_type,
                "param": settings.jaeger_sampler_rate,
            },
            "trace_id_header": settings.trace_id_header
        },
        service_name="post_service",
        validate=True,
        scope_manager=AsyncioScopeManager()
    )

    app.state.tracer = config.initialize_tracer()
    app.tracer = app.state.tracer


def http_404_requests():
    METRIC = Counter(
        "http_404_requests",
        "Number of times a 404 request has occured.",
        labelnames=("path",)
    )

    def instrumentation(info: Info):
        if info.response.status_code == 404:
            METRIC.labels(info.request.url).inc()

    return instrumentation


def http_unique_users():
    METRIC = Counter(
        "http_unique_users",
        "Number of unique http users.",
        labelnames=("user",)
    )

    def instrumentation(info: Info):
        try:
            user = f'{info.request.client.host} {info.request.headers["User-Agent"]}'
        except:
            user = f'{info.request.client.host} Unknown'
        METRIC.labels(user).inc()

    return instrumentation


instrumentator = Instrumentator(excluded_handlers=["/metrics"])
instrumentator.add(metrics.default())
instrumentator.add(metrics.combined_size())
instrumentator.add(http_404_requests())
instrumentator.add(http_unique_users())
instrumentator.instrument(app).expose(app)

setup_opentracing(app)


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Post(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    profile_id: int = Field(description='Profile ID')
    text: str = Field(...)
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "profile_id": "1",
                "text": "Neki <b> rich </b> text."
            }
        }


class PostResponse(BaseModel):
    id: str = Field(...)
    profile_id: int = Field(description='Profile ID')
    text: str = Field(...)
    likes: int = Field(description='Like count')
    dislikes: int = Field(description='Dislike count')
    opinion: str = Field(description='User opinion')


class Comment(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    profile_id: int = Field(description='Profile ID')
    author: str = Field(description='Comment author')
    post_id: str = Field(description='Post ID')
    text: str = Field(...)
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "profile_id": "1",
                "post_id": "000000000000000000000001",
                "text": "Neki text."
            }
        }


class CommentResponse(BaseModel):
    id: str = Field(...)
    profile_id: int = Field(description='Profile ID')
    author: str = Field(description='Comment author')
    post_id: str = Field(description='Post ID')
    text: str = Field(...)


class Like(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    profile_id: int = Field(description='Profile ID')
    post_id: str = Field(description='Post ID')
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "profile_id": "1",
                "post_id": "000000000000000000000001",
            }
        }


class Dislike(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    profile_id: int = Field(description='Profile ID')
    post_id: str = Field(description='Post ID')
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "profile_id": "1",
                "post_id": "000000000000000000000001",
            }
        }


class NavigationLinksPost(BaseModel):
    base: str = Field('http://localhost:8010/api/posts', description='API base URL')
    prev: Optional[str] = Field(None, description='Link to the previous page')
    next: Optional[str] = Field(None, description='Link to the next page')


class NavigationLinksComment(BaseModel):
    base: str = Field('http://localhost:8010/api/comments', description='API base URL')
    prev: Optional[str] = Field(None, description='Link to the previous page')
    next: Optional[str] = Field(None, description='Link to the next page')


class ResponsePost(BaseModel):
    results: List[PostResponse]
    links: NavigationLinksPost
    offset: int
    limit: int
    size: int
    
    
class ResponseStats(BaseModel):
    likes: int
    dislikes: int
    opinion: str


class ResponseComment(BaseModel):
    results: List[CommentResponse]
    links: NavigationLinksComment
    offset: int
    limit: int
    size: int


def register_kafka_producer():
    global kafka_producer
    while True:
        try:
            kafka_producer = KafkaProducer(bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            break
        except:
            time.sleep(3)


def record_action(status: int, message: str, span):
    print("{0:10}{1}".format('ERROR:' if status >= 400 else 'INFO:', message))
    span.set_tag('http_status', status)
    span.set_tag('message', message)


def record_event(type: str, data: dict):
    kafka_producer.send(KAFKA_EVENTS_TOPIC, {
        'type': type,
        'data': data
    })


def get_current_user_id(request: Request):
    try:
        return jwt.decode(request.headers['Authorization'], JWT_SECRET, algorithms=[JWT_ALGORITHM])['id']
    except:
        return None


def get_current_user_username(request: Request):
    try:
        return jwt.decode(request.headers['Authorization'], JWT_SECRET, algorithms=[JWT_ALGORITHM])['username']
    except:
        return None


def get_stats(profile_id: int, post_id: str):
    likes = len(list(like_col.find({"post_id": post_id})))
    dislikes = len(list(dislike_col.find({"post_id": post_id})))
    opinion = "neither"
    
    if likes != 0:
        opinion = "liked" if len(list(like_col.find({"$and": [{"profile_id": profile_id}, {"post_id": post_id}]}))) != 0 else "neither"
    if dislikes != 0 and opinion == "neither":
        opinion = "disliked" if len(list(dislike_col.find({"$and": [{"profile_id": profile_id}, {"post_id": post_id}]}))) != 0 else "neither"
    
    return likes, dislikes, opinion


def get_posts(offset: int = 0, limit: int = 7, profile_id: int = -1, link: str = 'posts', my_id: int = -1):
    total_posts = len(list(post_col.find({"profile_id": profile_id})))
    posts = list(post_col.find({"profile_id": profile_id}).skip(offset).limit(limit))

    prev_link = f'/{link}/{profile_id}?offset={offset - limit}&limit={limit}' if offset - limit >= 0 else None
    next_link = f'/{link}/{profile_id}?offset={offset + limit}&limit={limit}' if offset + limit < total_posts else None
    links = NavigationLinksPost(prev=prev_link, next=next_link)

    results = []

    for p in posts:
        like_cnt, dislike_cnt, opinion_str = get_stats(my_id, str(p["_id"]))
        results.append(PostResponse(id=str(p["_id"]), text=p["text"], profile_id=p["profile_id"], likes=like_cnt, dislikes=dislike_cnt, opinion=opinion_str))
        post_col.insert_one({"proba": "proba"})
    
    return results, links


def get_posts_mine(offset: int = 0, limit: int = 7, profile_id: int = -1):
    total_posts = len(list(post_col.find({"profile_id": profile_id})))
    posts = list(post_col.find({"profile_id": profile_id}).skip(offset).limit(limit))

    prev_link = f'/posts/private/mine?offset={offset - limit}&limit={limit}' if offset - limit >= 0 else None
    next_link = f'/posts/private/mine?offset={offset + limit}&limit={limit}' if offset + limit < total_posts else None
    links = NavigationLinksPost(prev=prev_link, next=next_link)

    results = []

    for p in posts:
        like_cnt, dislike_cnt, opinion_str = get_stats(profile_id, str(p["_id"]))
        results.append(PostResponse(id=str(p["_id"]), text=p["text"], profile_id=p["profile_id"], likes=like_cnt, dislikes=dislike_cnt, opinion=opinion_str))
        post_col.insert_one({"proba": "proba"})
    
    return results, links  


def get_comments(offset: int = 0, limit: int = 7, post_id: str = '0', link: str = 'comments'):
    total_comments = len(list(comment_col.find({"post_id": post_id})))
    comments = list(comment_col.find({"post_id": post_id}).skip(offset).limit(limit))

    prev_link = f'/{link}/{post_id}?offset={offset - limit}&limit={limit}' if offset - limit >= 0 else None
    next_link = f'/{link}/{post_id}?offset={offset + limit}&limit={limit}' if offset + limit < total_comments else None
    links = NavigationLinksComment(prev=prev_link, next=next_link)

    results = []

    for c in comments:
        results.append(CommentResponse(id=str(c["_id"]), text=c["text"], profile_id=c["profile_id"], post_id=c["post_id"], author=c["author"]))

    return results, links    


@app.post(POSTS_URL, response_description="Create new post")
def create_post(request: Request, post: Post = Body(...)):
    with app.tracer.start_span('Create Post Request') as span:
        try:
            span.set_tag('http_method', 'POST')
            
            post.profile_id = get_current_user_id(request)
            post_col.insert_one(jsonable_encoder(post))
            
            kafka_producer.send(KAFKA_NOTIFICATIONS_TOPIC, {'type': 'post', 'user_id': post.profile_id, 'message': 'New post from ' + get_current_user_username(request)})            
            record_action(200, 'Request successful', span)
            record_event('Post Created', json_util.dumps(post))
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e


@app.get(POSTS_URL + "/{profile_id}", response_description="List all posts")
def list_posts(request: Request, offset: int = Query(0), limit: int = Query(7), profile_id: int = -1):
    with app.tracer.start_span('List Posts Request') as span:
        try:
            span.set_tag('http_method', 'GET')
            
            results, links = get_posts(offset, limit, profile_id, my_id=get_current_user_id(request))

            record_action(200, 'Request successful', span)
            return ResponsePost(results=results, links=links, offset=offset, limit=limit, size=len(results))
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e


@app.get(POSTS_URL + "/public/{profile_id}", response_description="List all public posts")
def list_posts_public(request: Request, offset: int = Query(0), limit: int = Query(7), profile_id: int = -1):
    with app.tracer.start_span('List Public Posts Request') as span:
        try:
            span.set_tag('http_method', 'GET')
            
            results, links = get_posts(offset, limit, profile_id, 'posts/public', my_id=get_current_user_id(request))

            record_action(200, 'Request successful', span)
            return ResponsePost(results=results, links=links, offset=offset, limit=limit, size=len(results))
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e


@app.get(POSTS_URL + "/private/mine", response_description="List my posts")
def list_posts_mine(request: Request, offset: int = Query(0), limit: int = Query(7)):
    with app.tracer.start_span('List My Posts Request') as span:
        try:
            span.set_tag('http_method', 'GET')
            
            results, links = get_posts_mine(offset, limit, int(get_current_user_id(request)))

            record_action(200, 'Request successful', span)
            return ResponsePost(results=results, links=links, offset=offset, limit=limit, size=len(results))
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e


@app.post(COMMENTS_URL, response_description="Create new comment")
def create_comment(request: Request, comment: Comment = Body(...)):
    with app.tracer.start_span('Create Comment Request') as span:
        try:
            span.set_tag('http_method', 'POST')

            comment.profile_id = get_current_user_id(request)
            comment_col.insert_one(jsonable_encoder(comment))

            record_action(200, 'Request successful', span)
            record_event('Comment Created', json_util.dumps(comment))
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e


@app.get(COMMENTS_URL + "/{post_id}", response_description="List all comments")
def list_comments(request: Request, offset: int = Query(0), limit: int = Query(7), post_id: str = "0"):
    with app.tracer.start_span('List Comments Request') as span:
        try:
            span.set_tag('http_method', 'GET')

            results, links = get_comments(offset, limit, post_id)

            record_action(200, 'Request successful', span)
            return ResponseComment(results=results, links=links, offset=offset, limit=limit, size=len(results))
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e


@app.get(COMMENTS_URL + "/public/{post_id}", response_description="List all public comments")
def list_comments_public(request: Request, offset: int = Query(0), limit: int = Query(7), post_id: str = "0"):
    with app.tracer.start_span('List Public Comments Request') as span:
        try:
            span.set_tag('http_method', 'GET')

            results, links = get_comments(offset, limit, post_id, 'comments/public')
            
            record_action(200, 'Request successful', span)
            return ResponseComment(results=results, links=links, offset=offset, limit=limit, size=len(results))
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e


@app.post(POSTS_URL + "/like", response_description="Create new like")
def create_like(request: Request, like: Like = Body(...)):
    with app.tracer.start_span('Create Like Request') as span:
        try:
            span.set_tag('http_method', 'POST')

            like.profile_id = get_current_user_id(request)

            if len(list(like_col.find({"$and": [{"profile_id": like.profile_id}, {"post_id": like.post_id}]}))) == 0:
                like_col.insert_one(jsonable_encoder(like))
            
                if len(list(dislike_col.find({"$and": [{"profile_id": like.profile_id}, {"post_id": like.post_id}]}))) != 0:
                    dislike_col.delete_one({"$and": [{"profile_id": like.profile_id}, {"post_id": like.post_id}]})

            record_action(200, 'Request successful', span)
            record_event('Like Created', json_util.dumps(like))
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e


@app.post(POSTS_URL + "/dislike", response_description="Create new dislike")
def create_dislike(request: Request, dislike: Dislike = Body(...)):
    with app.tracer.start_span('Create Dislike Request') as span:
        try:
            span.set_tag('http_method', 'POST')

            dislike.profile_id = get_current_user_id(request)

            if len(list(dislike_col.find({"$and": [{"profile_id": dislike.profile_id}, {"post_id": dislike.post_id}]}))) == 0:
                dislike_col.insert_one(jsonable_encoder(dislike))
            
                if len(list(like_col.find({"$and": [{"profile_id": dislike.profile_id}, {"post_id": dislike.post_id}]}))) != 0:
                    like_col.delete_one({"$and": [{"profile_id": dislike.profile_id}, {"post_id": dislike.post_id}]})

            record_action(200, 'Request successful', span)
            record_event('Dislike Created', json_util.dumps(dislike))
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e


@app.delete(POSTS_URL + "/neither/{post_id}")
def delete_reactions(request: Request, post_id: str = "0"):
    with app.tracer.start_span('Delete Reactions Request') as span:
        try:
            span.set_tag('http_method', 'DELETE')

            profile_id = get_current_user_id(request)

            if len(list(dislike_col.find({"$and": [{"profile_id": profile_id}, {"post_id": post_id}]}))) != 0:
                dislike_col.delete_one({"$and": [{"profile_id": profile_id}, {"post_id": post_id}]})

            if len(list(like_col.find({"$and": [{"profile_id": profile_id}, {"post_id": post_id}]}))) != 0:
                like_col.delete_one({"$and": [{"profile_id": profile_id}, {"post_id": post_id}]})

            record_action(200, 'Request successful', span)
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e


@app.post(POSTS_URL + "/upload")
def upload(request: Request, file = File(...)):
    with app.tracer.start_span('Upload Image Request') as span:
        try:
            span.set_tag('http_method', 'POST')

            allowedFiles = {"image/jpeg", "image/png", "image/gif", "image/tiff", "image/bmp"}

            if file.content_type in allowedFiles:
                filename = str(uuid.uuid4())
                image_path = "download/" + filename + "_" + file.filename
                
                if not os.path.exists('download'):
                    os.makedirs('download')

                with open(image_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                
                image_path = image_path[::-1].replace(".", "_", 1)[::-1]
                
                record_action(200, 'Request successful', span)
                record_event('Image Saved', {'image_path': image_path})
                return {"imageUrl": "http://localhost:8000/" + image_path}
            else:
                raise HTTPException(status_code=400, detail='Unsupported image format')
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e


@app.get(POSTS_URL + "/download/{image_name}")
def download(request: Request, image_name: str = ""):
    with app.tracer.start_span('Download Image Request') as span:
        try:
            span.set_tag('http_method', 'GET')
            
            image_name = image_name[::-1].replace("_", ".", 1)[::-1]
            image_path = "download/" + image_name

            print(image_path)
            if os.path.isfile(image_path):
                record_action(200, 'Request successful', span)
                return FileResponse(image_path)
            else:
                raise HTTPException(status_code=404, detail='Image not found')
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e


def run_service():
    register_kafka_producer()
    uvicorn.run(app, host="0.0.0.0", port=8010)


if __name__ == '__main__':
    run_service()

