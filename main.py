from flask_admin import Admin
from flask import Flask, render_template, request, redirect, url_for
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import create_engine

from model import Book, Genre, db

API_ROOT = ''
BOOK_API_ROOT = API_ROOT + '/books/'
GENRE_API_ROOT = API_ROOT + '/genres/'
LIMIT = 15

app = Flask(__name__)
engine = create_engine("sqlite:///instance/project.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='База книг', template_mode='bootstrap3')

admin.add_view(ModelView(Book, db.session, name="Книги"))
admin.add_view(ModelView(Genre, db.session, name="Жанры"))


db.init_app(app)

with app.app_context():
    db.create_all()


@app.route(API_ROOT + '/main/', methods=["GET"])
def main():
    return render_template('main.html')

@app.route(BOOK_API_ROOT, methods=["GET"])
def list_books():
    """выводит N последних записей в порядке создания"""
    books = Book.query.order_by(Book.date_added.desc()).limit(LIMIT).all()
    title = 'Книги'
    return render_template('main_page_books.html', books=books, title=title)


@app.route(BOOK_API_ROOT + '/add/', methods=["GET", "POST"])
def add_book():
    """Добавление новой книги"""
    title = 'Добавить книгу'
    if request.method == "POST":
        print(request.form)
        book_title = request.form['book_title']
        author = request.form['author']
        genre_id = request.form['genre']
        if not title or not author or not genre_id:
            raise ValueError('Значения не заполнены')
        new_book = Book(
            title=book_title,
            author=author,
            genre_id=genre_id
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('list_books'))
    genre_list = Genre.query.all()
    return render_template(
    'add_book.html',
    genre_list=genre_list,
    title=title
    )


@app.route(BOOK_API_ROOT + '<book_id>/', methods = ['POST', 'GET'])
def book_page(book_id):
    '''Страница книги'''
    book = Book.query.get_or_404(book_id)
    title = f'Книга {book.title}'
    if request.method == 'POST' and request.form['save'] == 'confirmed':
        try:
            print(request.form)
            print(request.form['is_read'])
            print(request.form['save'])
            if request.form['is_read']:
                book.is_read = True
                print(book.id, book.is_read)
        except Exception:
            book.is_read = False

        db.session.commit()
    return render_template('book_page.html', book=book, title=title)


@app.route(GENRE_API_ROOT)
def list_genres():
    '''список всех жанров'''
    genres = Genre.query.all()
    title = 'Жанры'
    return render_template('main_page_genres.html', genres=genres, title=title)


@app.route(GENRE_API_ROOT + '/add/', methods=["GET", "POST"])
def add_genre():
    title = 'Добавить жанр'
    '''Добавление нового жанра'''
    if request.method == "POST":
        print(request.form)
        genre = request.form['new_genre']
        if not genre:
            raise ValueError('Значения не заполнены')
        new_genre = Genre(genre=genre)
        db.session.add(new_genre)
        db.session.commit()
        return redirect(url_for('list_genres'))
    return render_template('add_genre.html', title=title)


@app.route(GENRE_API_ROOT + '/<genre_id>/')
def list_books_by_genre(genre_id):
    '''список всех книг данного жанра'''
    title = 'Жанры'
    genre = Genre.query.get_or_404(genre_id)
    return render_template(
        'genre_page.html',
        genre_name=genre.genre,
        books=genre.books_of_genre, title=title
    )


if __name__ == '__main__':
    app.run(debug=True)
