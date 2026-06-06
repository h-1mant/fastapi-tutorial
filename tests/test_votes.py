from app.test_db_connection import client
from dotenv import load_dotenv
from app.oauth2 import _auth_headers

load_dotenv()

# Tests are order-dependent: they follow the vote lifecycle for a single (user, post) pair.
# 1. No vote  → upvote    → 201  (vote now exists)
# 2. Vote     → upvote    → 400
# 3. Vote     → downvote  → 201  (vote removed)
# 4. No vote  → downvote  → 400

def test_upvote_success(_create_user, _create_post):
    response = client.post(
        "/vote",
        json={"post_id": _create_post["id"], "vote_dir": 1},
        headers=_auth_headers(user_id=_create_user["id"])
    )
    assert response.status_code == 201
    data = response.json()
    assert data["post_id"] == _create_post["id"]
    assert data["vote_dir"] == 1

def test_upvote_already_voted(_create_user, _create_post):
    response = client.post(
        "/vote",
        json={"post_id": _create_post["id"], "vote_dir": 1},
        headers=_auth_headers(user_id=_create_user["id"])
    )
    assert response.status_code == 400

def test_downvote_success(_create_user, _create_post):
    response = client.post(
        "/vote",
        json={"post_id": _create_post["id"], "vote_dir": 0},
        headers=_auth_headers(user_id=_create_user["id"])
    )
    assert response.status_code == 201
    data = response.json()
    assert data["post_id"] == _create_post["id"]
    assert data["vote_dir"] == 0
    
def test_downvote_not_voted(_create_user, _create_post):
    response = client.post(
        "/vote",
        json={"post_id": _create_post["id"], "vote_dir": 0},
        headers=_auth_headers(user_id=_create_user["id"])
    )
    assert response.status_code == 400


