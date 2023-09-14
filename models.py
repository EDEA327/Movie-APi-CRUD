from pydantic import BaseModel


class MovieCreate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str


# Variable global para realizar un seguimiento del último id asignado
last_movie_id = 8


def generate_movie_id():
    global last_movie_id
    last_movie_id += 1
    return last_movie_id
