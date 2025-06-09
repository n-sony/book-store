from flask import Flask

from config import config_by_name, is_dev

from .core.db_init import db, migrate
from .core.jwt_init import jwt_manager
from .routes import author_api_routes, book_api_routes, user_api_routes, web_routes


def create_app(config_name: str) -> Flask:
    """
    Application factory function.
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt_manager.init_app(app)

    with app.app_context():
        app.register_blueprint(
            author_api_routes.api_author_bp, url_prefix="/api/v1/authors/"
        )
        app.register_blueprint(book_api_routes.api_book_bp, url_prefix="/api/v1/books/")
        app.register_blueprint(user_api_routes.api_user_bp, url_prefix="/api/v1/users/")
        app.register_blueprint(web_routes.web_bp)

        if is_dev:
            db.create_all()

        return app
