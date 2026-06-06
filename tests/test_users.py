from app.test_db_connection import client
from dotenv import load_dotenv
from app.oauth2 import _auth_headers
import uuid

load_dotenv()

def test_create_user():
    # Use a unique email so this test is independent and re-runnable
    test_email, test_password = f"test_{uuid.uuid4()}@test.com", "test"
    response = client.post(
        "/users",
        json={"email": test_email, "password": test_password}
    )
    assert response.status_code == 200

def test_get_all_users():
    response = client.get("/users", headers=_auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) >= 1

def test_get_user_by_id_success(_create_user):
    response = client.get(f"/users/{_create_user['id']}", headers=_auth_headers(user_id=_create_user["id"]))
    assert response.status_code == 200

def test_get_user_by_id_not_found(_create_user):
    response = client.get("/users/999999", headers=_auth_headers(user_id=_create_user["id"]))
    assert response.status_code == 404

def test_get_user_by_id_not_authorized(_create_user):
    response = client.get(f"/users/{_create_user['id']}")  # no auth headers
    assert response.status_code == 401

def test_update_password_success(_create_user):
    response = client.put(
        "/users/password",
        json={"current_password": _create_user["password"], "new_password": "new_password"},
        headers=_auth_headers(user_id=_create_user["id"])
    )
    assert response.status_code == 200

def test_update_password_wrong_current(_create_user):
    response = client.put(
        "/users/password",
        json={"current_password": "wrong_password", "new_password": "doesnt_matter"},
        headers=_auth_headers(user_id=_create_user["id"])
    )
    assert response.status_code == 401

def test_update_password_not_authorized(_create_user):
    response = client.put(
        "/users/password",
        json={"current_password": _create_user["password"], "new_password": "doesnt_matter"}
    )  # no auth headers
    assert response.status_code == 401







    
    
