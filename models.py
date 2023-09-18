from pydantic import BaseModel, Field

# Variable global para realizar un seguimiento del último id asignado
last_movie_id = 2


def generate_movie_id():
    global last_movie_id
    last_movie_id += 1
    return last_movie_id


class Movie(BaseModel):
    id: int = generate_movie_id()
    title: str = Field(min_length=5, max_length=20)
    overview: str = Field(min_length=5, max_length=30)
    year: int = Field(min_length=4, le=2023)
    rating: float = Field(le=10.0)
    category: str

    class Config:
        schema_extra = {
            "example": {
                "id": generate_movie_id(),
                "title": "A movie",
                "overview": "Starring Erick Escobar",
                "year": 2022,
                "category": "Acción"
            }

        }
