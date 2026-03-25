"""
Here is your opportunity to keep learning!

1. Create a new route called Users.

2. Then create 2 new API Endpoints

get_user: this endpoint should return all information about the user that is currently logged in.

change_password: this endpoint should allow a user to change their current password.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pydantic import BaseModel, Field
from ..models import Todos, User
from ..db import db_dependency
from starlette import status
from .auth import get_current_user, bcrypt_context

router = APIRouter(
    prefix="/users",
    tags=["users"]
)



user_dependency = Annotated[dict, Depends(get_current_user)]


class UserVerificationRequest(BaseModel):
    password: str
    new_password: str = Field(min_length=8)

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    user_infos = db.query(User).filter(User.id == user.get('id')).first()
    
    return user_infos

@router.put("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency, db:db_dependency, user_verification_request: UserVerificationRequest):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    user_infos = db.query(User).filter(User.id == user.get('id')).first()
    if not bcrypt_context.verify(user_verification_request.password, user_infos.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error on password verification")
    user_infos.hashed_password = bcrypt_context.hash(user_verification_request.new_password)
    db.add(user_infos)
    db.commit()

@router.put("/update-phone/", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone(user:user_dependency, db:db_dependency, phone_number: str = Query(min_length=10, max_length=15  )):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    user_infos = db.query(User).filter(User.id == user.get('id')).first()
    user_infos.phone_number = phone_number
    db.add(user_infos)
    db.commit()

