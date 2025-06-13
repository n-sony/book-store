from flask import Blueprint, jsonify, request

from app.services.users_service import UserService

api_auth_bp = Blueprint("api_auth_bp", __name__)


@api_auth_bp.route("", methods=["POST"])
def create_users():
    data = request.get_json()
    required_fields = ["username", "role_name", "password", "email"]
    if not data or not all(field in data for field in required_fields):
        return jsonify(
            {
                "error": '''
            Missing required fields: "email", "username", 
            "role_name", "password"'''
            }
        ), 400
    try:
        user = UserService.create_user(
            username=data.get("username"),
            role_name=data.get("role"),
            password=data.get("password"),
            email=data.get("email"),
        )
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_auth_bp.route("/login", methods=["POST"])
def login_users():
    data = request.get_json()
    required_fields = ["username", "password"]
    if not data or not all(field in data for field in required_fields):
        return jsonify(
            {"error": "Missing required fields: 'username', 'password'"}
        ), 400
    try:
        user = UserService.login(
            username=data.get("username"),
            password=data.get("password"),
        )
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
