from .utils import *
from jose import jwt
from datetime import datetime, timedelta, timezone
import pytest
from fastapi import HTTPException


def test_authenticate_user(test_user):
    bd =SessionLocalTest()

    authenticated_user = authenticate_user(bd, test_user.username, 'hashed')
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username


    non_existing_user =  authenticate_user(bd, 'wrongUser', 'hashed')
    assert  not non_existing_user

    wrong_password_user =  authenticate_user(bd, test_user.username, 'hashedwrong')
    assert  not non_existing_user 


def test_create_acces_token(test_user):
    username = "testuser"
    user_id = "1"   
    role = "user"
    expires_delta =  timedelta(days=1)

    token = create_access_token(username,user_id,role, expires_delta)

    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM, options={'verify_signature': False})


    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():

    encode = {'sub':'testuser', 'id':1, 'role':'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token)

    assert user == {'username': 'testuser', 'id': 1, 'role': 'admin'}


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    
    encode = {'role':'user'}

    token = jwt.encode(encode,SECRET_KEY, algorithm=ALGORITHM)

    with  pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == 'could not validate user'



