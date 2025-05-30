from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services.authors_service import AuthorService
from app.services.books_service import BookService

web_bp = Blueprint("web_bp", __name__, template_folder="../templates")


@web_bp.route("/")
def home():
    return render_template("home.html", title="Welcome to the BookShop")


# --- Author Web Routes ---
@web_bp.route("/authors")
def list_authors():
    authors = AuthorService.get_all_authors()
    return render_template(
        "authors/authors_list.html", authors=authors, title="Authors"
    )


@web_bp.route("/authors/<int:author_id>")
def author_detail(author_id):
    author = AuthorService.get_author_by_id(author_id)
    if not author:
        flash("Author not found.", "error")
        return redirect(url_for("web_bp.list_authors"))
    # Optionally fetch books by this author to display
    # books = BookService.get_books_by_author_id(author_id)
    return render_template(
        "authors/author_detail.html", author=author, title=author.name
    )


@web_bp.route("/authors/new", methods=["GET", "POST"])
def new_author():
    if request.method == "POST":
        name = request.form.get("name")
        bio = request.form.get("bio")
        if not name:
            flash("Author name is required.", "warning")
        else:
            try:
                AuthorService.create_author(name=name, bio=bio)
                flash(f'Author "{name}" created successfully!', "success")
                return redirect(url_for("web_bp.list_authors"))
            except ValueError as e:
                flash(str(e), "error")
    return render_template(
        "authors/author_form.html",
        title="New Author",
        form_action=url_for("web_bp.new_author"),
    )


@web_bp.route("/authors/<int:author_id>/edit", methods=["GET", "POST"])
def edit_author(author_id):
    author = AuthorService.get_author_by_id(author_id)
    if not author:
        flash("Author not found.", "error")
        return redirect(url_for("web_bp.list_authors"))

    if request.method == "POST":
        name = request.form.get("name")
        bio = request.form.get("bio")
        if not name:
            flash("Author name is required.", "warning")
        else:
            try:
                AuthorService.update_author(author_id, name=name, bio=bio)
                flash(f'Author "{name}" updated successfully!', "success")
                return redirect(url_for("web_bp.author_detail", author_id=author_id))
            except ValueError as e:
                flash(str(e), "error")
    return render_template(
        "authors/author_form.html",
        title=f"Edit {author.name}",
        author=author,
        form_action=url_for("web_bp.edit_author", author_id=author_id),
    )


@web_bp.route(
    "/authors/<int:author_id>/delete", methods=["POST"]
)  # Use POST for delete actions
def delete_author(author_id):
    author = AuthorService.get_author_by_id(author_id)
    if author:
        try:
            AuthorService.delete_author(author_id)
            flash(
                f'Author "{author.name}" and their books deleted successfully!',
                "success",
            )
        except Exception as e:  # Catch potential DB errors if any
            flash(f"Error deleting author: {str(e)}", "error")
    else:
        flash("Author not found.", "error")
    return redirect(url_for("web_bp.list_authors"))


# --- Book Web Routes ---
@web_bp.route("/books")
def list_books():
    books = BookService.get_all_books()
    return render_template("books/books_list.html", books=books, title="Books")


@web_bp.route("/books/<int:book_id>")
def book_detail(book_id):
    book = BookService.get_book_by_id(book_id)
    if not book:
        flash("Book not found.", "error")
        return redirect(url_for("web_bp.list_books"))
    return render_template("books/book_detail.html", book=book, title=book.title)


@web_bp.route("/books/new", methods=["GET", "POST"])
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
                return redirect(url_for("web_bp.list_books"))
            except ValueError as e:
                flash(str(e), "error")
    return render_template(
        "books/book_form.html",
        title="New Book",
        authors=authors,
        form_action=url_for("web_bp.new_book"),
    )


@web_bp.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    book = BookService.get_book_by_id(book_id)
    if not book:
        flash("Book not found.", "error")
        return redirect(url_for("web_bp.list_books"))

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
                return redirect(url_for("web_bp.book_detail", book_id=book_id))
            except ValueError as e:
                flash(str(e), "error")
    return render_template(
        "books/book_form.html",
        title=f"Edit {book.title}",
        book=book,
        authors=authors,
        form_action=url_for("web_bp.edit_book", book_id=book_id),
    )


@web_bp.route("/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    book = BookService.get_book_by_id(book_id)
    if book:
        BookService.delete_book(book_id)
        flash(f'Book "{book.title}" deleted successfully!', "success")
    else:
        flash("Book not found.", "error")
    return redirect(url_for("web_bp.list_books"))
