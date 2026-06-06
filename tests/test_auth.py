from app.test_db_connection import client
from dotenv import load_dotenv

load_dotenv()

def test_login_invalid_username(_create_user):
    # Test login via invalid username
    test_invalid_login = client.post("/login", data={"username": "random@test.com", "password": _create_user["password"]})
    assert test_invalid_login.status_code == 403

def test_login_invalid_password(_create_user):
    # Test login via invalid password
    test_invalid_login = client.post("/login", data={"username": _create_user["email"], "password": "random"})
    assert test_invalid_login.status_code == 403

def test_login_success(_create_user):
    # Test login via valid credentials    
    test_valid_login = client.post("/login", data={"username": _create_user["email"], "password": _create_user["password"]})
    assert test_valid_login.status_code == 200
    assert "access_token" in test_valid_login.json()
