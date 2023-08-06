from pymongo import MongoClient
import requests
import json
import pytest
import time
from post_service.main import JWT_SECRET, JWT_ALGORITHM
import jwt


POSTS_URL = 'http://localhost:8010/api/posts'
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


@pytest.fixture(scope="session", autouse=True)
def before_tests(request):
    time.sleep(10)


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
