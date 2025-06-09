from flask import Blueprint, jsonify, request

from app.services.authors_service import AuthorService
from app.services.books_service import BookService

api_author_bp = Blueprint("api_author_bp", __name__)


@api_author_bp.route("", methods=["POST"])
def create_author_api():
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "Author name is required"}), 400
    try:
        author = AuthorService.create_author(name=data["name"], bio=data.get("bio"))
        return jsonify(author.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@api_author_bp.route("", methods=["GET"])
def get_authors_api():
    authors = AuthorService.get_all_authors()
    return jsonify([author.to_dict() for author in authors]), 200


@api_author_bp.route("<int:author_id>", methods=["GET"])
def get_author_api(author_id):
    author = AuthorService.get_author_by_id(author_id)
    if author:
        return jsonify(author.to_dict()), 200
    return jsonify({"error": "Author not found"}), 404


@api_author_bp.route("<int:author_id>", methods=["PUT"])
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


@api_author_bp.route("<int:author_id>", methods=["DELETE"])
def delete_author_api(author_id):
    if AuthorService.delete_author(author_id):
        return jsonify({"message": "Author deleted successfully"}), 200
    return jsonify({"error": "Author not found or could not be deleted"}), 404


@api_author_bp.route("<int:author_id>/books", methods=["GET"])
def get_books_by_author_api(author_id):
    author = AuthorService.get_author_by_id(author_id)
    if not author:
        return jsonify({"error": "Author not found"}), 404
    books = BookService.get_books_by_author_id(author_id)
    return jsonify([book.to_dict() for book in books]), 200
