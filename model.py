from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String)
    author = db.Column(db.String)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'))

    def __repr__(self):
        return f'Название: {self.title}. Автор: {self.author}'


class Genre(db.Model):
    genre_id = db.Column(db.Integer, primary_key=True, nullable=False)
    genre = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'{self.genre}'


