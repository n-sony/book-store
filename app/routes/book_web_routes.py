from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services.authors_service import AuthorService
from app.services.books_service import BookService

web_books_bp = Blueprint("web_books_bp", __name__, template_folder="../templates")


@web_books_bp.route("")
def list_books():
    books = BookService.get_all_books()
    return render_template("books/books_list.html", books=books, title="Books")


@web_books_bp.route("/<int:book_id>")
def book_detail(book_id):
    book = BookService.get_book_by_id(book_id)
    if not book:
        flash("Book not found.", "error")
        return redirect(url_for("web_books_bp.list_books"))
    return render_template("books/book_detail.html", book=book, title=book.title)


@web_books_bp.route("/new", methods=["GET", "POST"])
def new_book():
    authors = AuthorService.get_all_authors()  # For dropdown
    if request.method == "POST":
        title = request.form.get("title")
        author_id = request.form.get("author_id", type=int)
        isbn = request.form.get("isbn")
        publication_year = request.form.get("publication_year", type=int)
        price = request.form.get("price", type=float)

        if not title or not author_id:
            flash("Book title and author are required.", "warning")
        else:
            try:
                BookService.create_book(title, author_id, isbn, publication_year, price)
                flash(f'Book "{title}" created successfully!', "success")
                return redirect(url_for("web_books_bp.list_books"))
            except ValueError as e:
                flash(str(e), "error")
    return render_template(
        "books/book_form.html",
        title="New Book",
        authors=authors,
        form_action=url_for("web_books_bp.new_book"),
    )


@web_books_bp.route("/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    book = BookService.get_book_by_id(book_id)
    if not book:
        flash("Book not found.", "error")
        return redirect(url_for("web_books_bp.list_books"))

    authors = AuthorService.get_all_authors()  # For dropdown
    if request.method == "POST":
        title = request.form.get("title")
        author_id = request.form.get("author_id", type=int)
        isbn = request.form.get("isbn")
        publication_year = request.form.get("publication_year", type=int)
        price = request.form.get("price", type=float)

        if not title or not author_id:
            flash("Book title and author are required.", "warning")
        else:
            try:
                BookService.update_book(
                    book_id, title, author_id, isbn, publication_year, price
                )
                flash(f'Book "{title}" updated successfully!', "success")
                return redirect(url_for("web_books_bp.book_detail", book_id=book_id))
            except ValueError as e:
                flash(str(e), "error")
    return render_template(
        "books/book_form.html",
        title=f"Edit {book.title}",
        book=book,
        authors=authors,
        form_action=url_for("web_books_bp.edit_book", book_id=book_id),
    )


@web_books_bp.route("/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    book = BookService.get_book_by_id(book_id)
    if book:
        BookService.delete_book(book_id)
        flash(f'Book "{book.title}" deleted successfully!', "success")
    else:
        flash("Book not found.", "error")
    return redirect(url_for("web_books_bp.list_books"))
