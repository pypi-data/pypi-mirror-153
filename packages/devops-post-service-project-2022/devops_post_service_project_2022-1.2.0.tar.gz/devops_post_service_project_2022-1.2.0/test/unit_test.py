from fastapi.testclient import TestClient
import post_service
from post_service.main import app, POSTS_URL, COMMENTS_URL, JWT_SECRET, JWT_ALGORITHM, get_stats
from mock import patch
import bson
import mongomock
import jwt
import json


class TestKP:
    def send(self, topic, data):
        pass


client = TestClient(app)
db = mongomock.MongoClient().post
post_col = db.post
comment_col = db.comment
like_col = db.like
dislike_col = db.dislike
testKP = TestKP()


def object_id_from_int(n):
    s = str(n)
    s = '0' * (24 - len(s)) + s
    return s


def generate_auth():
    return {'Authorization': jwt.encode({'id': 0}, JWT_SECRET, algorithm=JWT_ALGORITHM)}


def reset_colections():
    post_col.drop()
    comment_col.drop()
    like_col.drop()
    dislike_col.drop()


def get_stats_mock(profile_id: int, post_id: str):
    return 0, 0, "neither"

@patch("post_service.main.like_col", like_col)
@patch("post_service.main.dislike_col", dislike_col)
def test_get_stats_liked():
    like_col.insert_one({"profile_id": 0, "post_id": object_id_from_int(1)})

    with patch.object(like_col, "find", wraps=like_col.find) as like_db_spy:        
        with patch.object(dislike_col, "find", wraps=dislike_col.find) as dislike_db_spy:        
            likes, dislikes, opinion = get_stats(0, object_id_from_int(1))
            like_db_spy.assert_called()
            dislike_db_spy.assert_called()

            assert likes == 1
            assert dislikes == 0
            assert opinion == "liked"

    reset_colections()


@patch("post_service.main.like_col", like_col)
@patch("post_service.main.dislike_col", dislike_col)
def test_get_stats_disliked():
    dislike_col.insert_one({"profile_id": 0, "post_id": object_id_from_int(1)})

    with patch.object(like_col, "find", wraps=like_col.find) as like_db_spy:        
        with patch.object(dislike_col, "find", wraps=dislike_col.find) as dislike_db_spy:        
            likes, dislikes, opinion = get_stats(0, object_id_from_int(1))
            like_db_spy.assert_called()
            dislike_db_spy.assert_called()

            assert likes == 0
            assert dislikes == 1
            assert opinion == "disliked"

    reset_colections()


@patch("post_service.main.like_col", like_col)
@patch("post_service.main.dislike_col", dislike_col)
def test_get_stats_neither():
    with patch.object(like_col, "find", wraps=like_col.find) as like_db_spy:        
        with patch.object(dislike_col, "find", wraps=dislike_col.find) as dislike_db_spy:        
            likes, dislikes, opinion = get_stats(0, object_id_from_int(1))
            like_db_spy.assert_called()
            dislike_db_spy.assert_called()

            assert likes == 0
            assert dislikes == 0
            assert opinion == "neither"

    reset_colections()


@patch("post_service.main.post_col", post_col)
@patch("post_service.main.get_stats", get_stats_mock)
def test_list_posts():
    post_col.insert_one({"profile_id": 0, "text": "text1"})

    with patch.object(post_col, "find", wraps=post_col.find) as db_spy:
        with patch.object(post_service.main, "get_stats", wraps=post_service.main.get_stats) as stats_spy:
            res = client.get(f'{POSTS_URL}/0?offset=0&limit=10', headers=generate_auth())
            assert res.status_code == 200
            db_spy.assert_called()
            db_spy.assert_called_with({"profile_id": 0})
            stats_spy.assert_called()
            
    reset_colections()
