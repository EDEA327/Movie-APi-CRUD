from typing import List, Union

from fastapi import FastAPI, Body, HTTPException, Path, Query, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from config.database import Session, Base, engine
from jwt_manager import create_token, JwtBearer
from models.models import Movie, MovieCategory, User, MovieUpdate
from models.movie import MovieModel
from middelwares.error_handler import ErrorHandler

app = FastAPI(title='My Movie App', version='0.0.1', description='Una api de introducción a FastAPI')
Base.metadata.create_all(bind=engine)
app.add_middleware(ErrorHandler)


@app.get("/", tags=['home'], status_code=200)
def root():
    return HTMLResponse('<h1>Hola soy un html response</h1>')


@app.post('/login', tags=['auth'], status_code=200)
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return token


@app.get("/movies", tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JwtBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = jsonable_encoder(db.query(MovieModel).all())

    return result


@app.get("/movies/{movie_id}", tags=['movies'], response_model=Movie, status_code=200,
         dependencies=[Depends(JwtBearer())])
def get_movie_by_id(movie_id: int = Path(ge=1, le=100)) -> Movie:
    db: Session = Session()
    result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not result:
        raise HTTPException(status_code=404, detail=f'No se encontró la película con el id {movie_id}')

    return result


@app.get("/movies/", tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JwtBearer())])
def get_movies_by_category(category: MovieCategory = Query(min_length=5, max_length=15)) -> List[Movie]:
    db: Session = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        raise HTTPException(status_code=404, detail=f'No se encontró la categoría {category}')
    return result


@app.post("/movies", tags=['movies'], status_code=201, response_model=None, dependencies=[Depends(JwtBearer())])
def create_movie(movie: Movie) -> Union[str, HTTPException]:
    try:
        db: Session = Session()
        # Verifica si ya existe una película con el mismo id
        existing_movie = db.query(MovieModel).filter_by(id=movie.id).first()
        if existing_movie:
            raise HTTPException(status_code=400, detail=f'Ya existe una película con el ID {movie.id}')

        # Crea una nueva película en la base de datos
        new_movie = MovieModel(**movie.model_dump())
        db.add(new_movie)
        db.commit()

        return f'Película {movie.title} añadida correctamente'

    except Exception as e:
        # Maneja cualquier error inesperado
        db.rollback()  # Revierte la transacción en caso de error
        raise HTTPException(status_code=500, detail=f'Error al procesar la solicitud: {str(e)}')


@app.put("/movies/{id}", tags=["movies"], status_code=200, dependencies=[Depends(JwtBearer())])
def update_movie(movie_id: int, movie_update: MovieUpdate = Body(...)):
    db: Session = Session()
    result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not result:
        raise HTTPException(status_code=404, detail=f'No se encontró la película con el id {movie_id}')

    result.title = movie_update.title
    result.overview = movie_update.overview
    result.year = movie_update.year
    result.rating = movie_update.rating
    result.category = movie_update.category

    db.commit()

    return f'Se ha modificado con éxito'


@app.delete("/movies/{id}", tags=["movies"], status_code=200, dependencies=[Depends(JwtBearer())])
def delete_movie(movie_id: int):
    db: Session = Session()
    result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not result:
        raise HTTPException(status_code=404, detail=f'No existe película con el id {movie_id}')

    db.delete(result)
    db.commit()

    return {"message": f"Película con el id {movie_id} eliminada correctamente"}
