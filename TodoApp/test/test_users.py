from .utils import *

def test_get_users(test_user, test_user_return):
    response = client.get("/users/me")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_user_return

def test_change_password(test_user):
    response = client.put("/users/change-password", json={"password": "hashed", "new_password": "newhashed"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_current_password(test_user):
    response = client.put("/users/change-password", json={"password": "falsehashed", "new_password": "newhashed"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail':'Error on password verification'}


def test_change_phone_number_change_sucess(test_user):
    response = client.put('/users/update-phone/?phone_number=2222222222')
    assert response.status_code == status.HTTP_204_NO_CONTENT

