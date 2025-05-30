from app import db
from app.models.authors import Author
from app.models.books import Book


class BookService:
    @staticmethod
    def get_all_books():
        return Book.query.all()

    @staticmethod
    def get_book_by_id(book_id):
        return Book.query.get(book_id)

    @staticmethod
    def create_book(title, author_id, isbn=None, publication_year=None, price=None):
        author = Author.query.get(author_id)
        if not author:
            raise ValueError(f"Author with id {author_id} not found.")
        if isbn and Book.query.filter_by(isbn=isbn).first():
            raise ValueError(f"Book with ISBN '{isbn}' already exists.")

        new_book = Book(
            title=title,
            author_id=author_id,
            isbn=isbn,
            publication_year=publication_year,
            price=price,
        )
        db.session.add(new_book)
        db.session.commit()
        return new_book

    @staticmethod
    def update_book(
        book_id,
        title=None,
        author_id=None,
        isbn=None,
        publication_year=None,
        price=None,
    ):
        book = Book.query.get(book_id)
        if not book:
            return None

        if title:
            book.title = title
        if author_id:
            author = Author.query.get(author_id)
            if not author:
                raise ValueError(f"Author with id {author_id} not found.")
            book.author_id = author_id
        if isbn:
            existing_book = Book.query.filter(
                Book.isbn == isbn, Book.id != book_id
            ).first()
            if existing_book:
                raise ValueError(f"Another book with ISBN '{isbn}' already exists.")
            book.isbn = isbn
        if publication_year:
            book.publication_year = publication_year
        if price is not None:
            book.price = price

        db.session.commit()
        return book

    @staticmethod
    def delete_book(book_id):
        book = Book.query.get(book_id)
        if not book:
            return False
        db.session.delete(book)
        db.session.commit()
        return True

    @staticmethod
    def get_books_by_author_id(author_id):
        return Book.query.filter_by(author_id=author_id).all()
