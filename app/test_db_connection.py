from app.main import app
from app.db_connection import get_session
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient as TestClient
import os

test_engine = create_engine(os.getenv("TEST_DB_CONN_STRING"))

def override_get_session():
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)