import pytest
import uuid
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.test_db_connection import client, test_engine
from app.oauth2 import _auth_headers

@pytest.fixture(scope="module")
def _create_user():
    test_email = f"test_{uuid.uuid4()}@test.com"
    test_pwd = "test"
    response = client.post("/users", json={"email": test_email, "password": test_pwd})
    data = response.json()
    yield {"id": data["id"], "email": test_email, "password": test_pwd}
    # Cleanup: remove the user after all tests in the module complete
    with Session(test_engine) as session:
        session.execute(text("DELETE FROM users WHERE email = :email"), {"email": test_email})
        session.commit()

@pytest.fixture(scope="module")
def _create_post(_create_user):
    test_title, test_content, test_published = "test_post_title","test_post_content",False
    response = client.post(
        "/posts",
        json={"title": test_title,
              "content": test_content,
              "published": test_published,
        },
        headers=_auth_headers(user_id=_create_user["id"])
    )
    data = response.json()
    yield {"id": data["id"], "title": test_title, "content": test_content, "published": test_published}
    # Cleanup: remove the post after all tests in the module complete
    with Session(test_engine) as session:
        session.execute(text("DELETE FROM posts WHERE id = :id"), {"id": data["id"]})
        session.commit()