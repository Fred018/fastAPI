from fastapi import FastAPI, Request, status
from .models import Base
from .database import  engine
from .routers import auth, todo, admin, users

from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)


app.mount('/static', StaticFiles(directory='TodoApp/static'), name='static')

@app.get('/')
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(admin.router)

app.include_router(users.router)

app.include_router(auth.router)

app.include_router(todo.router)


