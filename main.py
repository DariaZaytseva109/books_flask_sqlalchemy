from datetime import date
from flask import Flask, render_template, request
from model import Book, Genre, db

API_ROOT = '/api/v1'
BOOK_API_ROOT = API_ROOT + '/book/'
GENRE_API_ROOT = API_ROOT + '/genre/'
LIMIT = 10

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route(BOOK_API_ROOT, methods=["GET"])
def list_books():
    '''view главной страницы,
    который выводит 15 последних записей в порядке создания'''
    books = Book.query.order_by(Book.date_added.desc()).limit(LIMIT).all()
    title = 'Книги'
    return render_template('main_page_books.html', books=books, title=title)


@app.route(BOOK_API_ROOT + '/add/', methods=["GET", "POST"])
def add_book():
    title = 'Добавить книгу'
    '''Добавление новой книги'''
    if request.method == "POST":
        print(request.form)
        title = request.form['title']
        author = request.form['author']
        genre_id = request.form['genre']
        if not title or not author or not genre_id:
            raise ValueError('Значения не заполнены')
        new_book = Book(
            title=title,
            author=author,
            genre_id = genre_id
        )
        db.session.add(new_book)
        db.session.commit()
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
