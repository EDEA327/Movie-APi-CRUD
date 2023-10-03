from models.movie import MovieModel


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
