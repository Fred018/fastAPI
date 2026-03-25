from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from ..db import db_dependency
from pydantic import BaseModel, Field
from ..models import User
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import  jwt, JWTError

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY = '4c6fad488207c4df0486240aba21772122cb8ceffe215545b956f6ce15ce7e90'
ALGORITHM = "HS256"



bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")




class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password:str
    role: str
    phone_number: str = Field(min_length=10, max_length=15)

class TokenRequest(BaseModel):
    access_token: str
    token_type: str



templates = Jinja2Templates(directory="TodoApp/templates")
### app.mount('/static', StaticFiles(directory='TodoApp/static'), name='static')
###pages
@router.get('/login-page')
def render_login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@router.get('/register-page')
def render_login_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})



##endpoint
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        role: str = payload.get('role')
        if username is None and user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user")
        return {'username': username, 'id': user_id, 'role': role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user")



def authenticate_user(db, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta:timedelta):
    
    encode  = {'sub': username, 'id': user_id, 'role': role}
    expire = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expire})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    user = User(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
        is_active=True,
        phone_number=create_user_request.phone_number
    )
    db.add(user)
    db.commit() 

@router.post("/login", response_model=TokenRequest)
async def login_foraccess_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    
    user  = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user")
    
    token = create_access_token(form_data.username, user.id, user.role, expires_delta=timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}