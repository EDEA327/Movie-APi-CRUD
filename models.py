from pydantic import BaseModel, Field


class Movie(BaseModel):
    id: int
    title: str = Field(min_length=5, max_length=20)
    overview: str = Field(min_length=5, max_length=30)
    year: int = Field(le=2023, ge=1900)
    rating: float = Field(ge=0, le=10.0)
    category: str = Field(max_length=15)

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
