from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title='My Movie App', version='0.0.1', description='Una api de introducción a Fast API')

# Lista de películas
movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Navi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'
    },
    {
        'id': 2,
        'title': 'Titanic',
        'overview': "Un joven artista se enamora de una mujer de alta sociedad abordo del Titanic...",
        'year': '1997',
        'rating': 7.8,
        'category': 'Drama'
    },
    {
        'id': 3,
        'title': 'Matrix',
        'overview': "Un hacker descubre que la realidad que conoce es una simulación...",
        'year': '1999',
        'rating': 8.7,
        'category': 'Ciencia Ficción'
    },
    {
        'id': 4,
        'title': 'El Padrino',
        'overview': "La historia de una poderosa familia de la mafia italiana en Estados Unidos...",
        'year': '1972',
        'rating': 9.2,
        'category': 'Crimen'
    },
    {
        'id': 5,
        'title': 'Star Wars',
        'overview': "Una epopeya espacial sobre un joven llamado Luke Skywalker...",
        'year': '1977',
        'rating': 8.6,
        'category': 'Ciencia Ficción'
    },
    {
        'id': 6,
        'title': 'El Señor de los Anillos',
        'overview': "Un viaje épico para destruir un anillo mágico que puede llevar a la destrucción del mundo...",
        'year': '2001',
        'rating': 8.8,
        'category': 'Fantasía'
    },
    {
        'id': 7,
        'title': 'Jurassic Park',
        'overview': "Un parque de diversiones con dinosaurios se convierte en una pesadilla...",
        'year': '1993',
        'rating': 8.1,
        'category': 'Aventura'
    },
    {
        'id': 8,
        'title': 'Forrest Gump',
        'overview': "La vida de un hombre con discapacidades intelectuales que afecta la historia de Estados Unidos...",
        'year': '1997',
        'rating': 8.8,
        'category': 'Drama'
    }
]


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
