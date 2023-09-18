from typing import List

from fastapi import FastAPI, Body, HTTPException, Path, Query
from fastapi.responses import HTMLResponse

from data import movies_list
from models import Movie, MovieCategory

app = FastAPI(title='My Movie App', version='0.0.1', description='Una api de introducción a FastAPI')


@app.get("/", tags=['home'])
def root():
    return HTMLResponse('<h1>Hola soy un html response</h1>')


@app.get("/movies", tags=['movies'], response_model=List[Movie])
def get_movies() -> List[Movie]:
    return movies_list


@app.get("/movies/{id}", tags=['movies'], response_model=Movie)
def get_movie_by_id(movie_id: int = Path(ge=1, le=100)) -> Movie:
    for item in movies_list:
        if item['id'] == movie_id:
            return item
    raise HTTPException(status_code=404, detail=f'No se encontró la película con el id {movie_id}')


@app.get("/movies/", tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: MovieCategory = Query(min_length=5, max_length=15)) -> List[Movie]:
    filtered_movies = [movie for movie in movies_list if movie['category'] == category]
    if filtered_movies:
        return filtered_movies
    raise HTTPException(status_code=404, detail=f'No hay películas para la categoría {category}')


@app.post("/movies", tags=['movies'])
def create_movie(movie: Movie = Body(...)):
    # Verificar que no existe una película con el mismo id
    if any(existing_movie['id'] == movie.id for existing_movie in movies_list):
        raise HTTPException(status_code=400, detail=f"Ya existe una película con el ID {movie.id}.")

    new_movie = {
        'id': movie.id,
        'title': movie.title,
        'overview': movie.overview,
        'year': movie.year,
        'rating': movie.rating,
        'category': movie.category
    }
    movies_list.append(new_movie)
    return new_movie


@app.put("/movies/{id}", tags=["movies"])
def update_movie(movie_id: int, movie_update: Movie = Body(...)):
    for movie in movies_list:
        if movie['id'] == movie_id:
            # Actualiza los campos de la película con los datos proporcionados
            movie['title'] = movie_update.title
            movie['overview'] = movie_update.overview
            movie['year'] = movie_update.year
            movie['rating'] = movie_update.rating
            movie['category'] = movie_update.category
            return movie
    raise HTTPException(status_code=404, detail=f'No existe película con el id {movie_id}')


@app.delete("/movies/{id}", tags=["movies"])
def delete_movie(movie_id: int):
    initial_length = len(movies_list)
    movies_list[:] = [movie for movie in movies_list if movie['id'] != movie_id]  # Actualizar la lista original

    if len(movies_list) < initial_length:
        return {"message": f"Película con el id {movie_id} eliminada correctamente"}
    else:
        raise HTTPException(status_code=404, detail=f'No existe película con el id {movie_id}')
