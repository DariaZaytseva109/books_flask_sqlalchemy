from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String)
    author = db.Column(db.String)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id', ondelete='SET NULL'))
    genre_name = relationship('Genre', back_populates='books_of_genre')


    def __repr__(self):
        return f'Название: {self.title}. Автор: {self.author}'


class Genre(db.Model):
    genre_id = db.Column(db.Integer, primary_key=True, nullable=False)
    genre = db.Column(db.Integer, nullable=False)
    books_of_genre = relationship('Book', back_populates='genre_name')

    def __repr__(self):
        return f'{self.genre}'


