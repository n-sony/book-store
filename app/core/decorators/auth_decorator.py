from functools import wraps

from flask import current_app, flash, g, jsonify, redirect, request, session, url_for
from flask_jwt_extended import decode_token

from app.services.users_service import UserService


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("web_auth_bp.login"))
        return f(*args, **kwargs)

    return decorated_function


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            # Expected format: "Bearer <token>"
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            # Decode the token using the app's secret key
            data = decode_token(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            # Find the user and attach it to Flask's global 'g' object
            g.current_user = UserService.find_by_id(data["user_id"])
            if not g.current_user:
                return jsonify({"message": "User not found!"}), 401
        except Exception as e:
            return jsonify({"message": f"Invalid Token: {e}"}), 401

        return f(*args, **kwargs)

    return decorated
