from datetime import date, datetime
from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    birth_date: Mapped[datetime] = mapped_column()
    registration_date: Mapped[datetime] = mapped_column(default=date.today())

    def __repr__(self):
        return self.username


class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(30))
    genre_id: Mapped[int] = mapped_column(ForeignKey('genre.genre_id', ondelete='SET NULL'))
    date_added: Mapped[datetime] = mapped_column(default=date.today())
    is_read: Mapped[bool] = mapped_column(default=False)
    genre: Mapped["Genre"] = relationship(back_populates="books_of_genre")
    rating: Mapped[int] = mapped_column(Integer, nullable=True)

    def __repr__(self):
        return f'Название: {self.title}. Автор: {self.author}'


class Genre(db.Model):
    genre_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    genre: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    books_of_genre: Mapped[List["Book"]] = relationship(back_populates="genre")

    def __repr__(self):
        return f'{self.genre}'
