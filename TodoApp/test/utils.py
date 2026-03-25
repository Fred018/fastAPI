from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi import status

from ..models import Todos, User

from ..db import get_db

from ..routers.auth import get_current_user, bcrypt_context, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM
from ..database import Base
from ..main import app

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


_db_path = os.path.join(os.path.dirname(__file__), "todoapp.db")
SQLALCHEMY_DB_URL = f"sqlite:///{_db_path}"


engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})

HASHED_PASSWORD = bcrypt_context.hash("hashed")

SessionLocalTest = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


client = TestClient(app)


def override_get_db():
    db = SessionLocalTest()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"id": 1, "sub": "testuser", "role": 'admin'}


app.dependency_overrides[get_current_user] = override_get_current_user

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def test_user():
    user = User(id=1, email="test@test.com", username="testuser",
                first_name="Test", last_name="User",
                hashed_password=HASHED_PASSWORD, is_active=True, role="admin",
                phone_number="1234567890")
    bd = SessionLocalTest()
    bd.add(user)
    bd.commit()
    yield user
    with SessionLocalTest() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()


@pytest.fixture
def test_todo(test_user):
    todo = Todos(title="learn to code",
                 description="Need to learn to code in order to get a job",
                 complete=False,
                 priority=5,
                 owner=test_user.id,
                 id=1)
    bd = SessionLocalTest()
    bd.add(todo)
    bd.commit()
    yield todo
    with SessionLocalTest() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

@pytest.fixture
def test_todo_return():
    return {
        "title": "learn to code",
        "description": "Need to learn to code in order to get a job",
        "complete": False,
        "priority": 5,
        "owner": 1,
        "id": 1
    }

@pytest.fixture
def test_user_return():
    return {
        "id": 1,
        "email": "test@test.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "is_active": True,
        "role": "admin",
        "hashed_password": HASHED_PASSWORD,
        "phone_number": "1234567890"
    }

