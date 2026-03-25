
from .utils import *
from fastapi import status


def test_read_all_authenticated(test_todo, test_todo_return):
    response = client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [test_todo_return]

def test_read_todo(test_todo, test_todo_return):
    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_todo_return

def test_read_todo_not_found():
    response = client.get("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo pas trouvé"}

def test_create_todo(test_user):
    request_data = {
        "title": "learn to code",
        "description": "Need to learn to code in order to get a job",
        "complete": False,
        "priority": 5
    }

    response = client.post("/todos/", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = SessionLocalTest()
    todo_in_db = db.query(Todos).filter(Todos.owner == test_user.id).first()
    assert todo_in_db is not None
    assert todo_in_db.title == request_data["title"]
    assert todo_in_db.description == request_data["description"]
    assert todo_in_db.complete == request_data["complete"]
    assert todo_in_db.priority == request_data["priority"]
    db.delete(todo_in_db)
    db.commit()

def test_update_todo(test_todo):
    request_data = {
        "title": "changed title",
        "description": "Need to learn to code in order to get a job",
        "complete": True,
        "priority": 2
    }

    response = client.put("/todos/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = SessionLocalTest()
    updated_todo = db.query(Todos).filter(Todos.id == test_todo.id).first()
    assert updated_todo is not None
    assert updated_todo.complete == request_data["complete"]
    assert updated_todo.priority == request_data["priority"]
    assert updated_todo.title == request_data["title"]
    assert updated_todo.description == request_data["description"]
    db.delete(updated_todo)
    db.commit()


def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "changed title",
        "description": "Need to learn to code in order to get a job",
        "complete": True,
        "priority": 2
    }

    response = client.put("/todos/999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo with id 999 not found"}


def test_delete_todo(test_todo):
    todo_id = test_todo.id
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = SessionLocalTest()
    deleted_todo = db.query(Todos).filter(Todos.id == todo_id).first()
    assert deleted_todo is None

def test_delete_todo_not_found():
    response = client.delete("/todos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo with id 999 not found"}

