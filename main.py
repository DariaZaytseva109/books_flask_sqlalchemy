from flask import Flask, render_template

from model import Book, Genre, db


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    db.session.add(Book(id=1, title='Мастер и Маргарита', author='М. Булгаков', genre_id=1))
    db.session.add(Book(id=2, title='Три товарища', author='Э.М. Ремарк', genre_id=1))
    db.session.add(Book(id=3, title='Герой нашего времени', author='М. Лермонтов', genre_id=1))
    db.session.add(Book(id=4, title='Стихи', author='А. Пушкин', genre_id=2))
    db.session.add(Genre(genre_id=1, genre='Роман'))
    db.session.add(Genre(genre_id=2, genre='Стихи'))
    db.session.commit()

API_ROOT = '/api/v1'
BOOK_API_ROOT = API_ROOT + '/book/'
GENRE_API_ROOT = API_ROOT + '/genre/'



@app.route(BOOK_API_ROOT)
def list_books():
    '''view главной страницы приложения, который выводит 15 последних записей из Book в порядке создания - новые записи вверху списка'''
    books = Book.query.all()
    return render_template('main_page_books.html', books=books)



@app.route(GENRE_API_ROOT)
def list_genres():
    '''список всех жанров'''
    genres = Genre.query.all()
    return render_template('main_page_genres.html', genres=genres)



@app.route(GENRE_API_ROOT + '/<genre_id>/')
def list_books_by_genre(genre_id):
    '''список всех книг данного жанра'''
    pass




if __name__ == '__main__':
    app.run()
