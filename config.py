import logging
import os
from datetime import timedelta

from dotenv import load_dotenv

from app.core.exception import DatabaseTypeException

load_dotenv()

FLASK_ENV = os.environ.get("FLASK_ENV")


def database_string(db_type: str) -> str:
    match db_type:
        case "postgres":
            return "postgresql+psycopg2://"
        case "mysql":
            return "mysql://"
        case "sqlite":
            return "sqlite://"
        case "mongodb":
            return "mongod://"
        case _:
            raise DatabaseTypeException("Invalid choice")


class Config:
    try:
        SECRET_KEY = os.environ.get("SECRET_KEY")

        DATABASE_START_STRING = database_string(os.environ.get("DB_TYPE"))
        SQLALCHEMY_DATABASE_URI = f"{DATABASE_START_STRING}{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        JWT_EXPIRATION_DELTA = timedelta(hours=1)
    except DatabaseTypeException as e:
        logging.debug("Invalid database type")
        raise e


class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = False
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config_by_name(config_name: str) -> Config:
    return config_by_name.get(config_name, DevelopmentConfig)


def is_dev() -> bool:
    return FLASK_ENV == "development"


def is_prod() -> bool:
    return FLASK_ENV == "production"


def is_test() -> bool:
    return FLASK_ENV == "test"
