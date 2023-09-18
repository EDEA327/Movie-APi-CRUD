from enum import Enum

from pydantic import BaseModel, Field


class MovieCategory(str, Enum):
    action = "Acción"
    drama = "Drama"
    comedia = "Comedia"
    fiction = "Ciencia Ficción"
    other = "Otro"


class Movie(BaseModel):
    id: int
    title: str = Field(min_length=5, max_length=20)
    overview: str = Field(min_length=5, max_length=100)
    year: int = Field(le=2023, ge=1900)
    rating: float = Field(ge=0, le=10.0)
    category: MovieCategory = Field(max_length=15)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 3,
                "title": "A movie",
                "overview": "Starring Erick Escobar",
                "year": 2022,
                "rating": 10.0,
                "category": "Acción"
            }

        }
