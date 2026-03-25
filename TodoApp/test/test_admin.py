from .utils import *


def test_read_all(test_todo, test_todo_return):
    response = client.get ('/admin/todos')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [test_todo_return]




def test_delete_todo(test_todo):
    response = client.delete('/admin/todo/1')

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = SessionLocalTest()
    todo = db.query(Todos).filter(Todos.id == 1).first()
    assert todo is None


def test_delete_todo_not_found():
    response = client.delete('/admin/todo/999')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo with id 999 not found"}
