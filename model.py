from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Book(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    title = db.Column(db.String)
    author = db.Column(db.String(30))
    genre_id = db.Column(
        db.Integer,
        db.ForeignKey('genre.genre_id', ondelete='SET NULL')
    )
    genre_name = relationship(
        'Genre',
        back_populates='books_of_genre'
    )
    date_added = db.Column(db.Date, default=date.today())
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'Название: {self.title}. Автор: {self.author}'


class Genre(db.Model):
    genre_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    genre = db.Column(db.String(30), nullable=False)
    books_of_genre = relationship(
        'Book',
        back_populates='genre_name'
    )

    def __repr__(self):
        return f'{self.genre}'
