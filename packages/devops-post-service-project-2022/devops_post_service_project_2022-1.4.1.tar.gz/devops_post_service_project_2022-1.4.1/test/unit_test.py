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


@patch("post_service.main.comment_col", comment_col)
def test_list_comments():
    comment_col.insert_one({"profile_id": 0, "author": "a1", "post_id": object_id_from_int(1), "text": "text1"})

    with patch.object(comment_col, "find", wraps=comment_col.find) as db_spy:
        res = client.get(f'{COMMENTS_URL}/{object_id_from_int(1)}?offset=7&limit=10', headers=generate_auth())
        assert res.status_code == 200
        db_spy.assert_called()
        db_spy.assert_called_with({"post_id": object_id_from_int(1)})
            
    reset_colections()


@patch("post_service.main.like_col", like_col)
@patch("post_service.main.dislike_col", dislike_col)
@patch('post_service.main.kafka_producer', testKP)
def test_create_like_nothing():
    like_col.insert_one({"profile_id": 0, "post_id": object_id_from_int(1)})

    with patch.object(like_col, "find", wraps=like_col.find) as l_find_spy:
        with patch.object(like_col, "insert_one", wraps=like_col.insert_one) as l_insert_spy:
            with patch.object(dislike_col, "find", wraps=dislike_col.find) as dl_find_spy:
                with patch.object(dislike_col, "delete_one", wraps=dislike_col.delete_one) as dl_delete_spy:
                    data = {
                        "Id": "",
                        "post_id": object_id_from_int(1),
                        "profile_id": 0
                    }
                    res = client.post(f'{POSTS_URL}/like', headers=generate_auth(), json=data)
                    assert res.status_code == 200
                    l_find_spy.assert_called()
                    l_find_spy.assert_called_with({"$and": [{"profile_id": 0}, {"post_id": object_id_from_int(1)}]})
                    body = json.loads(res.text)
                    assert body is None
                    l_insert_spy.assert_not_called()
                    dl_find_spy.assert_not_called()
                    dl_delete_spy.assert_not_called()

    reset_colections()


@patch("post_service.main.like_col", like_col)
@patch("post_service.main.dislike_col", dislike_col)
@patch('post_service.main.kafka_producer', testKP)
def test_create_like_no_delete():
    with patch.object(like_col, "find", wraps=like_col.find) as l_find_spy:
        with patch.object(like_col, "insert_one", wraps=like_col.insert_one) as l_insert_spy:
            with patch.object(dislike_col, "find", wraps=dislike_col.find) as dl_find_spy:
                with patch.object(dislike_col, "delete_one", wraps=dislike_col.delete_one) as dl_delete_spy:
                    data = {
                        "Id": "",
                        "post_id": object_id_from_int(1),
                        "profile_id": 0
                    }
                    res = client.post(f'{POSTS_URL}/like', headers=generate_auth(), json=data)
                    assert res.status_code == 200
                    l_find_spy.assert_called()
                    l_find_spy.assert_called_with({"$and": [{"profile_id": 0}, {"post_id": object_id_from_int(1)}]})
                    l_insert_spy.assert_called()
                    dl_find_spy.assert_called()
                    dl_find_spy.assert_called_with({"$and": [{"profile_id": 0}, {"post_id": object_id_from_int(1)}]})
                    body = json.loads(res.text)
                    assert body is None
                    dl_delete_spy.assert_not_called()

    reset_colections()


@patch("post_service.main.like_col", like_col)
@patch("post_service.main.dislike_col", dislike_col)
@patch('post_service.main.kafka_producer', testKP)
def test_create_like_delete_dislike():
    dislike_col.insert_one({"profile_id": 0, "post_id": object_id_from_int(1)})

    with patch.object(like_col, "find", wraps=like_col.find) as l_find_spy:
        with patch.object(like_col, "insert_one", wraps=like_col.insert_one) as l_insert_spy:
            with patch.object(dislike_col, "find", wraps=dislike_col.find) as dl_find_spy:
                with patch.object(dislike_col, "delete_one", wraps=dislike_col.delete_one) as dl_delete_spy:
                    data = {
                        "Id": "",
                        "post_id": object_id_from_int(1),
                        "profile_id": 0
                    }
                    res = client.post(f'{POSTS_URL}/like', headers=generate_auth(), json=data)
                    assert res.status_code == 200
                    l_find_spy.assert_called()
                    l_find_spy.assert_called_with({"$and": [{"profile_id": 0}, {"post_id": object_id_from_int(1)}]})
                    l_insert_spy.assert_called()
                    dl_find_spy.assert_called()
                    dl_find_spy.assert_called_with({"$and": [{"profile_id": 0}, {"post_id": object_id_from_int(1)}]})
                    dl_delete_spy.assert_called()
                    body = json.loads(res.text)
                    assert body is None

    reset_colections()


@patch("post_service.main.like_col", like_col)
@patch("post_service.main.dislike_col", dislike_col)
@patch('post_service.main.kafka_producer', testKP)
def test_create_dislike_nothing():
    dislike_col.insert_one({"profile_id": 0, "post_id": object_id_from_int(1)})

    with patch.object(like_col, "find", wraps=like_col.find) as l_find_spy:
        with patch.object(like_col, "delete_one", wraps=like_col.delete_one) as l_delete_spy:
            with patch.object(dislike_col, "find", wraps=dislike_col.find) as dl_find_spy:
                with patch.object(dislike_col, "insert_one", wraps=dislike_col.insert_one) as dl_insert_spy:
                    data = {
                        "Id": "",
                        "post_id": object_id_from_int(1),
                        "profile_id": 0
                    }
                    res = client.post(f'{POSTS_URL}/dislike', headers=generate_auth(), json=data)
                    assert res.status_code == 200
                    dl_find_spy.assert_called()
                    dl_find_spy.assert_called_with({"$and": [{"profile_id": 0}, {"post_id": object_id_from_int(1)}]})
                    body = json.loads(res.text)
                    assert body is None
                    dl_insert_spy.assert_not_called()
                    l_find_spy.assert_not_called()
                    l_delete_spy.assert_not_called()

    reset_colections()


@patch("post_service.main.like_col", like_col)
@patch("post_service.main.dislike_col", dislike_col)
@patch('post_service.main.kafka_producer', testKP)
def test_create_dislike_no_delete():
    with patch.object(like_col, "find", wraps=like_col.find) as l_find_spy:
        with patch.object(like_col, "delete_one", wraps=like_col.delete_one) as l_delete_spy:
            with patch.object(dislike_col, "find", wraps=dislike_col.find) as dl_find_spy:
                with patch.object(dislike_col, "insert_one", wraps=dislike_col.insert_one) as dl_insert_spy:
                    data = {
                        "Id": "",
                        "post_id": object_id_from_int(1),
                        "profile_id": 0
                    }
                    res = client.post(f'{POSTS_URL}/dislike', headers=generate_auth(), json=data)
                    assert res.status_code == 200
                    dl_find_spy.assert_called()
                    dl_find_spy.assert_called_with({"$and": [{"profile_id": 0}, {"post_id": object_id_from_int(1)}]})
                    dl_insert_spy.assert_called()
                    l_find_spy.assert_called()
                    l_find_spy.assert_called_with({"$and": [{"profile_id": 0}, {"post_id": object_id_from_int(1)}]})
                    body = json.loads(res.text)
                    assert body is None
                    l_delete_spy.assert_not_called()

    reset_colections()


@patch("post_service.main.like_col", like_col)
@patch("post_service.main.dislike_col", dislike_col)
@patch('post_service.main.kafka_producer', testKP)
def test_create_dislike_delete_like():
    like_col.insert_one({"profile_id": 0, "post_id": object_id_from_int(1)})

    with patch.object(like_col, "find", wraps=like_col.find) as l_find_spy:
        with patch.object(like_col, "delete_one", wraps=like_col.delete_one) as l_delete_spy:
            with patch.object(dislike_col, "find", wraps=dislike_col.find) as dl_find_spy:
                with patch.object(dislike_col, "insert_one", wraps=dislike_col.insert_one) as dl_insert_spy:
                    data = {
                        "Id": "",
                        "post_id": object_id_from_int(1),
                        "profile_id": 0
                    }
                    res = client.post(f'{POSTS_URL}/dislike', headers=generate_auth(), json=data)
                    assert res.status_code == 200
                    dl_find_spy.assert_called()
                    dl_find_spy.assert_called_with({"$and": [{"profile_id": 0}, {"post_id": object_id_from_int(1)}]})
                    dl_insert_spy.assert_called()
                    l_find_spy.assert_called()
                    l_find_spy.assert_called_with({"$and": [{"profile_id": 0}, {"post_id": object_id_from_int(1)}]})
                    l_delete_spy.assert_called()
                    body = json.loads(res.text)
                    assert body is None

    reset_colections()