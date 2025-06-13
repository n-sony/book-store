from flask import Blueprint, jsonify, request

from app.core.decorators.auth_decorator import token_required
from app.services.books_service import BookService

api_book_bp = Blueprint("api_book_bp", __name__)


@api_book_bp.route("", methods=["POST"])
@token_required
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


@api_book_bp.route("", methods=["GET"])
def get_books_api():
    books = BookService.get_all_books()
    return jsonify([book.to_dict() for book in books]), 200


@api_book_bp.route("<int:book_id>", methods=["GET"])
def get_book_api(book_id):
    book = BookService.get_book_by_id(book_id)
    if book:
        return jsonify(book.to_dict()), 200
    return jsonify({"error": "Book not found"}), 404


@api_book_bp.route("<int:book_id>", methods=["PUT"])
@token_required
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


@api_book_bp.route("<int:book_id>", methods=["DELETE"])
@token_required
def delete_book_api(book_id):
    if BookService.delete_book(book_id):
        return jsonify({"message": "Book deleted successfully"}), 200
    return jsonify({"error": "Book not found or could not be deleted"}), 404
