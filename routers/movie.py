from typing import List, Union

from fastapi import APIRouter
from fastapi import Body, HTTPException, Path, Query, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from config.database import Session
from middelwares.jwt_manager import JwtBearer
from models.models import Movie, MovieCategory, MovieUpdate
from models.movie import MovieModel
from services.movie import MovieService

movie_router = APIRouter()


@movie_router.get("/movies", tags=['movies'], response_model=List[Movie], status_code=200,
                  dependencies=[Depends(JwtBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()

    return jsonable_encoder(result)


@movie_router.get("/movies/{movie_id}", tags=['movies'], response_model=Movie, status_code=200,
                  dependencies=[Depends(JwtBearer())])
def get_movie_by_id(movie_id: int = Path(ge=1, le=100)) -> Movie:
    db: Session = Session()
    result = MovieService(db).get_movie(movie_id)
    if not result:
        raise HTTPException(status_code=404, detail=f'No se encontró la película con el id {movie_id}')

    return result


@movie_router.get("/movies/", tags=['movies'], response_model=List[Movie], status_code=200,
                  dependencies=[Depends(JwtBearer())])
def get_movies_by_category(category: MovieCategory = Query(min_length=5, max_length=15)) -> List[Movie]:
    db: Session = Session()
    result = MovieService(db).category_filter(category)
    if not result:
        raise HTTPException(status_code=404, detail=f'No se encontró la categoría {category}')
    return result


@movie_router.post("/movies", tags=['movies'], status_code=201, response_model=None,
                   dependencies=[Depends(JwtBearer())])
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


@movie_router.put("/movies/{id}", tags=["movies"], status_code=200, dependencies=[Depends(JwtBearer())])
def update_movie(movie_id: int, movie_update: MovieUpdate = Body(...)):
    db: Session = Session()
    result = MovieService(db).get_movie(movie_id)
    if not result:
        raise HTTPException(status_code=404, detail=f'No se encontró la película con el id {movie_id}')

    result.title = movie_update.title
    result.overview = movie_update.overview
    result.year = movie_update.year
    result.rating = movie_update.rating
    result.category = movie_update.category

    db.commit()

    return f'Se ha modificado con éxito'


@movie_router.delete("/movies/{id}", tags=["movies"], status_code=200, dependencies=[Depends(JwtBearer())])
def delete_movie(movie_id: int):
    db: Session = Session()
    result = MovieService(db).get_movie(movie_id)
    if not result:
        raise HTTPException(status_code=404, detail=f'No existe película con el id {movie_id}')

    db.delete(result)
    db.commit()

    return {"message": f"Película con el id {movie_id} eliminada correctamente"}
