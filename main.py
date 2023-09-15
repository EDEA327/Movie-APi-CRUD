from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import HTMLResponse

from models import MovieCreate, MovieUpdate, generate_movie_id
from movies import movies_list

app = FastAPI(title='My Movie App', version='0.0.1', description='Una api de introducción a FastAPI')


@app.get("/", tags=['home'])
def root():
    return HTMLResponse('<h1>Hola soy un html response</h1>')


@app.get("/movies", tags=['movies'])
def get_movies():
    return movies_list


@app.get("/movies/{id}", tags=['movies'])
def get_movie_by_id(movie_id: int):
    for item in movies_list:
        if item['id'] == movie_id:
            return item
    raise HTTPException(status_code=404, detail=f'No se encontró la película con el id {movie_id}')


@app.get("/movies/", tags=['movies'])
def get_movies_by_category(category: str, year: str):
    filtered_movies = [movie for movie in movies_list if movie['category'] == category and movie['year'] == year]
    if filtered_movies:
        return filtered_movies
    raise HTTPException(status_code=404, detail=f'No hay películas para la categoría {category} y el año {year}')


@app.post("/movies", tags=['movies'])
def create_movie(movie: MovieCreate = Body(...)):
    movie_id = generate_movie_id()
    new_movie = {
        'id': movie_id,
        'title': movie.title,
        'overview': movie.overview,
        'year': movie.year,
        'rating': movie.rating,
        'category': movie.category
    }
    movies_list.append(new_movie)
    return new_movie


@app.put("/movies/{id}", tags=["movies"])
def update_movie(movie_id: int, movie_update: MovieUpdate = Body(...)):
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