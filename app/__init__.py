from flask import Flask

from config import config_by_name, is_dev

from .core.db_init import db, migrate
from .routes import api_routes, web_routes


def create_app(config_name: str) -> Flask:
    """
    Application factory function.
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        app.register_blueprint(api_routes.api_bp, url_prefix="/api/v1")
        app.register_blueprint(web_routes.web_bp)

        if is_dev:
            db.create_all()

        return app
