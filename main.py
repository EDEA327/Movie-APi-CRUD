from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from config.database import Base, engine
from middelwares.error_handler import ErrorHandler
from middelwares.jwt_manager import create_token
from models.models import User
from routers.movie import movie_router

app = FastAPI(title='My Movie App', version='0.0.1', description='Una api de introducción a FastAPI')
Base.metadata.create_all(bind=engine)
app.add_middleware(ErrorHandler)
app.include_router(movie_router)


@app.get("/", tags=['home'], status_code=200)
def root():
    return HTMLResponse('<h1>Hola soy un html response</h1>')


@app.post('/login', tags=['auth'], status_code=200)
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return token
