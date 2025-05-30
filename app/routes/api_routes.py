from flask import Blueprint, jsonify, request

from app.services.authors_service import AuthorService
from app.services.books_service import BookService

api_bp = Blueprint("api_bp", __name__)


@api_bp.route("/authors", methods=["POST"])
def create_author_api():
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "Author name is required"}), 400
    try:
        author = AuthorService.create_author(name=data["name"], bio=data.get("bio"))
        return jsonify(author.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@api_bp.route("/authors", methods=["GET"])
def get_authors_api():
    authors = AuthorService.get_all_authors()
    return jsonify([author.to_dict() for author in authors]), 200


@api_bp.route("/authors/<int:author_id>", methods=["GET"])
def get_author_api(author_id):
    author = AuthorService.get_author_by_id(author_id)
    if author:
        return jsonify(author.to_dict()), 200
    return jsonify({"error": "Author not found"}), 404


@api_bp.route("/authors/<int:author_id>", methods=["PUT"])
def update_author_api(author_id):
    data = request.get_json()
    try:
        author = AuthorService.update_author(
            author_id, name=data.get("name"), bio=data.get("bio")
        )
        if author:
            return jsonify(author.to_dict()), 200
        return jsonify({"error": "Author not found"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/authors/<int:author_id>", methods=["DELETE"])
def delete_author_api(author_id):
    if AuthorService.delete_author(author_id):
        return jsonify({"message": "Author deleted successfully"}), 200
    return jsonify({"error": "Author not found or could not be deleted"}), 404


@api_bp.route("/books", methods=["POST"])
def create_book_api():
    data = request.get_json()
    required_fields = ["title", "author_id"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields: title, author_id"}), 400
    try:
        book = BookService.create_book(
            title=data["title"],
            author_id=data["author_id"],
            isbn=data.get("isbn"),
            publication_year=data.get("publication_year"),
            price=data.get("price"),
        )
        return jsonify(book.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/books", methods=["GET"])
def get_books_api():
    books = BookService.get_all_books()
    return jsonify([book.to_dict() for book in books]), 200


@api_bp.route("/books/<int:book_id>", methods=["GET"])
def get_book_api(book_id):
    book = BookService.get_book_by_id(book_id)
    if book:
        return jsonify(book.to_dict()), 200
    return jsonify({"error": "Book not found"}), 404


@api_bp.route("/books/<int:book_id>", methods=["PUT"])
def update_book_api(book_id):
    data = request.get_json()
    try:
        book = BookService.update_book(
            book_id,
            title=data.get("title"),
            author_id=data.get("author_id"),
            isbn=data.get("isbn"),
            publication_year=data.get("publication_year"),
            price=data.get("price"),
        )
        if book:
            return jsonify(book.to_dict()), 200
        return jsonify({"error": "Book not found"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book_api(book_id):
    if BookService.delete_book(book_id):
        return jsonify({"message": "Book deleted successfully"}), 200
    return jsonify({"error": "Book not found or could not be deleted"}), 404


@api_bp.route("/authors/<int:author_id>/books", methods=["GET"])
def get_books_by_author_api(author_id):
    author = AuthorService.get_author_by_id(author_id)
    if not author:
        return jsonify({"error": "Author not found"}), 404
    books = BookService.get_books_by_author_id(author_id)
    return jsonify([book.to_dict() for book in books]), 200
