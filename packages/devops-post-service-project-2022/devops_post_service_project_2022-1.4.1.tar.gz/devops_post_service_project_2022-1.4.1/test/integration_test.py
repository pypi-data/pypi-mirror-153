from pymongo import MongoClient
import requests
import json
import pytest
import time
from post_service.main import JWT_SECRET, JWT_ALGORITHM
import jwt


POSTS_URL = 'http://localhost:8010/api/posts'
COMMENTS_URL = 'http://localhost:8010/api/comments'
client = MongoClient('mongodb://localhost:27017/post?authSource=admin', username='root', password='password')
db = client.post
post_col = db.post
comment_col = db.comment
like_col = db.like
dislike_col = db.dislike


def object_id_from_int(n):
    s = str(n)
    s = '0' * (24 - len(s)) + s
    return s


def generate_auth():
    return {'Authorization': jwt.encode({'id': 0, 'username': 'u1'}, JWT_SECRET, algorithm=JWT_ALGORITHM)}


def reset_posts(number_of_rows=0):
    post_col.drop()
    
    for i in range(number_of_rows):
        post = {
            "_id": object_id_from_int(i+1),
            "profile_id": 0,
            "text": f'text{i+1}'
        }
        post_col.insert_one(post)


def check_posts(posts: list, limit=7, offset_check=lambda x: x+1):
    assert len(posts) == limit
    for i in range(limit):
        assert posts[i]['id'] == object_id_from_int(offset_check(i))

        assert posts[i]['profile_id'] == 0
        assert posts[i]['text'] == f'text{offset_check(i)}'
    post_col.drop()


def reset_comments(number_of_rows=0):
    comment_col.drop()
    
    for i in range(number_of_rows):
        comment = {
            "_id": object_id_from_int(i+1),
            "post_id": object_id_from_int(100),
            "profile_id": 0,
            "text": f'text{i+1}',
            "author": f'a{i+1}'
        }
        comment_col.insert_one(comment)


def check_comments(comments: list, limit=7, offset_check=lambda x: x+1):
    assert len(comments) == limit
    for i in range(limit):
        assert comments[i]['id'] == object_id_from_int(offset_check(i))
        
        assert comments[i]['post_id'] == object_id_from_int(offset_check(100))
        assert comments[i]['profile_id'] == 0
        assert comments[i]['text'] == f'text{offset_check(i)}'
        assert comments[i]['author'] == f'text{offset_check(i)}'
    comment_col.drop()


def reset_likes(number_of_rows=0):
    like_col.drop()
    
    like = {
        "_id": object_id_from_int(1),
        "profile_id": 0,
        "post_id": object_id_from_int(100)
    }
    like_col.insert_one(like)


def reset_dislikes(number_of_rows=0):
    dislike_col.drop()
    
    like = {
        "_id": object_id_from_int(1),
        "profile_id": 0,
        "post_id": object_id_from_int(100)
    }
    dislike_col.insert_one(like)


@pytest.fixture(scope="session", autouse=True)
def before_tests(request):
    time.sleep(30)


def test_read_posts():
    reset_posts(10)
    res = requests.get(f'{POSTS_URL}/0', headers=generate_auth())
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] is None
    assert body['links']['next'] == '/posts/0?offset=7&limit=7'
    assert body['offset'] == 0
    assert body['limit'] == 7
    assert body['size'] == 7
    check_posts(body['results'])


def test_read_posts_with_offset():
    reset_posts(10)
    res = requests.get(f'{POSTS_URL}/0?offset=7', headers=generate_auth())
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] == '/posts/0?offset=0&limit=7'
    assert body['links']['next'] is None
    assert body['offset'] == 7
    assert body['limit'] == 7
    assert body['size'] == 3
    check_posts(body['results'], 3, lambda x: 8+x)


def test_read_posts_with_limit():
    reset_posts(10)
    res = requests.get(f'{POSTS_URL}/0?limit=10', headers=generate_auth())
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] is None
    assert body['links']['next'] is None
    assert body['offset'] == 0
    assert body['limit'] == 10
    assert body['size'] == 10
    check_posts(body['results'], 10)


def test_read_comments():
    reset_comments(10)
    res = requests.get(f'{COMMENTS_URL}/{object_id_from_int(100)}', headers=generate_auth())
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] is None
    assert body['links']['next'] == f'/comments/{object_id_from_int(100)}?offset=7&limit=7'
    assert body['offset'] == 0
    assert body['limit'] == 7
    assert body['size'] == 7
    check_posts(body['results'])


def test_read_comments_with_offset():
    reset_comments(10)
    res = requests.get(f'{COMMENTS_URL}/{object_id_from_int(100)}?offset=7', headers=generate_auth())
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] == f'/comments/{object_id_from_int(100)}?offset=0&limit=7'
    assert body['links']['next'] is None
    assert body['offset'] == 7
    assert body['limit'] == 7
    assert body['size'] == 3
    check_posts(body['results'], 3, lambda x: 8+x)


def test_read_comments_with_limit():
    reset_comments(10)
    res = requests.get(f'{COMMENTS_URL}/{object_id_from_int(100)}?limit=10', headers=generate_auth())
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] is None
    assert body['links']['next'] is None
    assert body['offset'] == 0
    assert body['limit'] == 10
    assert body['size'] == 10
    check_posts(body['results'], 10)


def test_create_like_nothing():
    reset_likes()
    dislike_col.drop()
    
    data = {
        "_id": object_id_from_int(2),
        "profile_id": 0,
        "post_id": object_id_from_int(200)
    }
    
    res = requests.post(f'{POSTS_URL}/like', json=data, headers=generate_auth())
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body is None
    likes = list(like_col.find({"$and": [{"profile_id": 0}, {"post_id": object_id_from_int(100)}]}))
    assert len(likes) == 1

    assert likes[0]['_id'] == object_id_from_int(1)
    assert likes[0]['profile_id'] == 0
    assert likes[0]['post_id'] == object_id_from_int(100)


def test_create_like_no_delete():
    like_col.drop()
    dislike_col.drop()
    
    data = {
        "_id": object_id_from_int(2),
        "profile_id": 0,
        "post_id": object_id_from_int(200)
    }
    
    res = requests.post(f'{POSTS_URL}/like', json=data, headers=generate_auth())
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body is None
    likes = list(like_col.find({"$and": [{"profile_id": 0}, {"post_id": object_id_from_int(200)}]}))
    assert len(likes) == 1

    assert likes[0]['_id'] == object_id_from_int(2)
    assert likes[0]['profile_id'] == 0
    assert likes[0]['post_id'] == object_id_from_int(200)


def test_create_like_delete_dislike():
    like_col.drop()
    reset_dislikes()
    
    data = {
        "_id": object_id_from_int(1),
        "profile_id": 0,
        "post_id": object_id_from_int(100)
    }
    
    res = requests.post(f'{POSTS_URL}/like', json=data, headers=generate_auth())
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body is None
    likes = list(like_col.find({"$and": [{"profile_id": 0}, {"post_id": object_id_from_int(100)}]}))
    assert len(likes) == 1

    assert likes[0]['_id'] == object_id_from_int(1)
    assert likes[0]['profile_id'] == 0
    assert likes[0]['post_id'] == object_id_from_int(100)
    
    assert len(list(dislike_col.find({"$and": [{"profile_id": 0}, {"post_id": object_id_from_int(100)}]}))) == 0


def test_create_dislike_nothing():
    reset_dislikes()
    like_col.drop()
    
    data = {
        "_id": object_id_from_int(2),
        "profile_id": 0,
        "post_id": object_id_from_int(200)
    }
    
    res = requests.post(f'{POSTS_URL}/dislike', json=data, headers=generate_auth())
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body is None
    dislikes = list(dislike_col.find({"$and": [{"profile_id": 0}, {"post_id": object_id_from_int(100)}]}))
    assert len(dislikes) == 1

    assert dislikes[0]['_id'] == object_id_from_int(1)
    assert dislikes[0]['profile_id'] == 0
    assert dislikes[0]['post_id'] == object_id_from_int(100)


def test_create_dislike_no_delete():
    dislike_col.drop()
    like_col.drop()
    
    data = {
        "_id": object_id_from_int(2),
        "profile_id": 0,
        "post_id": object_id_from_int(200)
    }
    
    res = requests.post(f'{POSTS_URL}/dislike', json=data, headers=generate_auth())
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body is None
    dislikes = list(dislike_col.find({"$and": [{"profile_id": 0}, {"post_id": object_id_from_int(200)}]}))
    assert len(dislikes) == 1

    assert dislikes[0]['_id'] == object_id_from_int(2)
    assert dislikes[0]['profile_id'] == 0
    assert dislikes[0]['post_id'] == object_id_from_int(200)


def test_create_dislike_delete_like():
    dislike_col.drop()
    reset_likes()
    
    data = {
        "_id": object_id_from_int(1),
        "profile_id": 0,
        "post_id": object_id_from_int(100)
    }
    
    res = requests.post(f'{POSTS_URL}/dislike', json=data, headers=generate_auth())
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body is None
    dislikes = list(dislike_col.find({"$and": [{"profile_id": 0}, {"post_id": object_id_from_int(100)}]}))
    assert len(dislikes) == 1

    assert dislikes[0]['_id'] == object_id_from_int(1)
    assert dislikes[0]['profile_id'] == 0
    assert dislikes[0]['post_id'] == object_id_from_int(100)
    
    assert len(list(like_col.find({"$and": [{"profile_id": 0}, {"post_id": object_id_from_int(100)}]}))) == 0
