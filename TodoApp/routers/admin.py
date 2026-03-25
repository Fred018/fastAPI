from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from ..models import Todos
from ..db import db_dependency
from starlette import status
from .auth import get_current_user


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    
    todos = db.query(Todos).all()
    return todos


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency, db: db_dependency, todo_id:int = Path(gt=0)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo is None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {todo_id} not found")
    
    db.delete(todo) 
    db.commit()