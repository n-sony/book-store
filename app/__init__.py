from flask import Flask

from config import config_by_name, is_dev

from .core.db_init import db, migrate
from .core.jwt_init import jwt_manager
from .routes import (
    auth_api_routes,
    auth_web_routes,
    author_api_routes,
    author_web_routes,
    book_api_routes,
    book_web_routes,
    home_web_routes,
)


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
        app.register_blueprint(auth_api_routes.api_auth_bp, url_prefix="/api/v1/auth/")
        app.register_blueprint(author_web_routes.web_authors_bp, url_prefix="/authors")
        app.register_blueprint(book_web_routes.web_books_bp, url_prefix="/books")
        app.register_blueprint(auth_web_routes.web_auth_bp, url_prefix="/auth")
        app.register_blueprint(home_web_routes.web_home_bp, url_prefix="/")

        if is_dev():
            db.create_all()

        from .seeds.roles import seed_roles

        @app.cli.command("seed-db")
        def seed_db_command():
            """Seeds the database with initial data (e.g., roles)."""
            seed_roles()
            print("Database seeding process finished.")

        return app
