from functools import wraps

from flask import flash, g, jsonify

from app.core.decorators.auth_decorator import token_required


def role_required(role_name):
    """
    Decorator for web routes (session-based) to require a specific role.
    Must be used *after* @login_required.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.user:
                flash("User not found", "error")
            if not g.user.has_role(role_name):
                flash("Forbidden ressource user not allowed", "error")
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def api_role_required(role_name):
    """
    Decorator for API routes to require a specific role from a JWT.
    Must be used *after* @token_required (or it can wrap it).
    """

    def decorator(f):
        @wraps(f)
        @token_required  # This ensures we have a valid token and user first
        def decorated_function(current_user_from_token, *args, **kwargs):
            if not current_user_from_token.has_role(role_name):
                return jsonify(
                    {"message": f"Permission denied: Requires '{role_name}' role."}
                ), 403
            return f(current_user_from_token, *args, **kwargs)

        return decorated_function

    return decorator
    return decorator
