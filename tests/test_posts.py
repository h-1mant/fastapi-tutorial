from app.test_db_connection import client
from dotenv import load_dotenv
from app.oauth2 import _auth_headers
import uuid

load_dotenv()

def test_create_post(_create_user):
    test_title="test_title"
    test_content="test_content"
    test_published=False
    test_user_id=_create_user["id"]

    response = client.post(
        "/posts",
        json={"title": test_title,"content":test_content,"published":test_published,"user_id":test_user_id},
        headers=_auth_headers(user_id=_create_user["id"])
    )
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == test_title
    assert data["content"] == test_content
    assert data["published"] == test_published
    assert data["user_id"] == test_user_id

def test_get_all_posts(_create_user,_create_post):
    response = client.get("/posts", headers=_auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert len(data["posts"]) >= 1

def test_get_my_posts(_create_user, _create_post):
    response = client.get("/posts/my_posts", headers=_auth_headers(user_id=_create_user["id"]))
    assert response.status_code == 200
    data = response.json()
    assert len(data["posts"]) >= 1

def test_get_post_by_id_success(_create_user, _create_post):
    response = client.get(f"/posts/{_create_post['id']}", headers=_auth_headers(user_id=_create_user["id"]))
    assert response.status_code == 200

def test_get_post_by_id_not_found(_create_user):
    response = client.get("/posts/999999", headers=_auth_headers(user_id=_create_user["id"]))
    assert response.status_code == 404

def test_get_post_by_id_not_authorized(_create_post):
    response = client.get(f"/posts/{_create_post['id']}")  # no auth headers
    assert response.status_code == 401

def test_update_post(_create_user, _create_post):
    updated_title = "updated_title"
    updated_content = "updated_content"
    response = client.put(
        f"/posts/{_create_post['id']}",
        json={"title": updated_title, "content": updated_content},
        headers=_auth_headers(user_id=_create_user["id"])
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == updated_title
    assert data["content"] == updated_content

def test_delete_post(_create_user):
    # Create a dedicated post so deletion doesn't affect other tests using _create_post
    response = client.post(
        "/posts",
        json={"title": "to_delete", "content": "to_delete_content", "published": False},
        headers=_auth_headers(user_id=_create_user["id"])
    )
    assert response.status_code == 201
    post_id = response.json()["id"]

    response = client.delete(
        f"/posts/{post_id}",
        headers=_auth_headers(user_id=_create_user["id"])
    )
    assert response.status_code == 204






