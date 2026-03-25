from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Request
from pydantic import BaseModel, Field
from ..models import Todos
from ..db import db_dependency
from starlette import status
from .auth import get_current_user

from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

templates = Jinja2Templates(directory="TodoApp/templates")


router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

user_dependency = Annotated[dict, Depends(get_current_user)]



class TodoRequest(BaseModel):
    title: str  = Field(min_length=10)
    description: str = Field(min_length=1, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = False






def redirec_to_login():
    redirect_responce = RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)
    redirect_responce.delete_cookie(key='access_token')
    return redirect_responce

        
### app.mount('/static', StaticFiles(directory='TodoApp/static'), name='static')
###pages
@router.get('/todo-page')
async def render_todo_page(request: Request, db: db_dependency):

    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirec_to_login()
        
        todos = db.query(Todos).filter(Todos.owner == user.get('id')).all()

        return templates.TemplateResponse('todo.html', {'request':request, 'todos': todos, 'user': user})
    except:
        return redirec_to_login()
        

@router.get('/add-todo-page')
async def render_add_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirec_to_login()

        return templates.TemplateResponse('add-todo.html', {'request':request, 'user': user})
    except:
        return redirec_to_login()

@router.get('/edit-todo-page/{todo_id}')
async def render_edit_todo_page(request: Request, todo_id: int, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirec_to_login()
        
        todo_to_update = db.query(Todos).\
                filter(Todos.id == todo_id).\
                filter(Todos.owner == user.get('id')).\
                first()

        return templates.TemplateResponse('edit-todo.html', {'request':request, 'user': user, 'todo':todo_to_update})
    except:
        return redirec_to_login()



##endpoint

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    todos = db.query(Todos).filter(Todos.owner == user.get('id')).all()
    return todos

@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency,db:db_dependency,todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    result = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner == user.get('id')).first()

    if result is not None:
        return result
    raise HTTPException(status_code=404, detail="Todo pas trouvé")

@router.post("/", status_code =status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,
                        db: db_dependency, 
                      todo_request: TodoRequest):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    new_todo = Todos(**todo_request.model_dump(), owner = user.get('id'))

    db.add(new_todo)
    db.commit()

@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency,
                    db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    todo_to_update = db.query(Todos).\
                filter(Todos.id == todo_id).\
                filter(Todos.owner == user.get('id')).\
                first()
    if not todo_to_update:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    
    todo_to_update.title = todo_request.title
    todo_to_update.description = todo_request.description   
    todo_to_update.priority = todo_request.priority
    todo_to_update.complete = todo_request.complete 
    db.add(todo_to_update)
    db.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db:db_dependency, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized")

    todo_to_delete = db.query(Todos).\
                filter(Todos.id == todo_id).\
                filter(Todos.owner == user.get('id')).\
                first()

    if not todo_to_delete:
        raise HTTPException(status_code=404, 
                            detail=f"Todo with id {todo_id} not found")
    
    db.delete(todo_to_delete)
    db.commit()