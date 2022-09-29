import hashlib

from setup_db import db


class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Director(db.Model):
    __tablename__ = 'director'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey(f"{Genre.__tablename__}.id"))
    director_id = db.Column(db.Integer, db.ForeignKey(f"{Director.__tablename__}.id"))
    genre = db.relationship("Genre")
    director = db.relationship("Director")


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    role = db.Column(db.String)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = self.get_hash()

    def get_hash(self):
        return hashlib.md5(self.password.encode('utf-8')).hexdigest()

    def compare_passwords(self, other_password) -> bool:
        new_password_hash = hashlib.md5(other_password.encode('utf-8')).hexdigest()
        return new_password_hash == self.password
