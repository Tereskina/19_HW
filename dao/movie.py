from dao.model.models import Movie


class MovieDAO:

    def __init__(self, session):
        self.session = session

    def get_all_movies(self):
        return self.session.query(Movie).all()

    def get_movie_by_movie_id(self, movie_id):
        return self.session.query(Movie).filter(Movie.id == movie_id).one()

    def get_movies_by_many_filters(self, **kwargs):
        # return dict where values are not None
        return self.session.query(Movie).filter_by(
            **{k: v for k, v in kwargs.items() if v is not None}
        ).all()

    def create(self, **kwargs) -> bool:
        try:
            self.session.add(
                Movie(
                    **kwargs
                )
            )
            self.session.commit()
            return True

        except Exception as e:
            print(f"Failed to add new movie\n{e}")
            self.session.rollback()
            return False

    def update(self, **kwargs):
        try:
            self.session.query(Movie).filter(Movie.id == kwargs.get("id")).update(
                kwargs
            )
            self.session.commit()
        except Exception as e:
            print(f"Failed to change movie\n{e}")
            self.session.rollback()

    def delete(self, movie_id):
        try:
            self.session.query(Movie).filter(Movie.id == movie_id).delete()
            self.session.commit()
        except Exception as e:
            print(f"Failed to delete movie\n{e}")
            self.session.rollback()
