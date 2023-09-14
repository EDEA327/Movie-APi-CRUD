from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from models import MovieCreate, generate_movie_id

from movies import movies

app = FastAPI(title='My Movie App', version='0.0.1', description='Una api de introducción a Fast API')


@app.get("/", tags=['home'])
def root():
    return HTMLResponse('<h1>Hola soy un html response</h1>')


@app.get("/movies", tags=['movies'])
def get_movies():
    return movies


@app.get("/movies/{id}", tags=['movies'])
def get_movie_by_id(pk: int):
    for item in movies:
        if item['id'] == pk:
            return item
    return f'No se encontró el id {pk}'


@app.get("/movies/", tags=['movies'])
def get_movies_by_category(category: str, year: str):
    # Filtrar las películas por categoría y año
    filtered_movies = [movie for movie in movies if movie['category'] == category and movie['year'] == year]
    # Si hay películas que cumplen (o sea la lista tiene elementos)
    if filtered_movies:
        return filtered_movies
    return f'No hay películas para la categoría {category} y el año {year}'


@app.post("/movies/", tags=['movies'])
def create_movie(id: int, title: str, overview: str, year: int):
    pass
