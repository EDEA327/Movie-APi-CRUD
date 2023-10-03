from models.movie import MovieModel
from schemas.movie import Movie, MovieUpdate


class MovieService:
    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result

    def get_movie(self, movie_id):
        result = self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()
        return result

    def category_filter(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result

    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.model_dump())
        self.db.add(new_movie)
        self.db.commit()

        return

    def update_movie(self, movie_id: int, data: MovieUpdate):
        movie = self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()
        movie.title = data.title
        movie.overview = data.overview
        movie.year = data.year
        movie.rating = data.rating
        movie.category = data.category

        self.db.commit()

        return

    def delete_movie(self, movie_id: int):
        self.db.query(MovieModel).filter(MovieModel.id == movie_id).delete()
        self.db.commit()
        return
