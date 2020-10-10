"""Flask configuration variables."""
from os import environ, path, getenv
from dotenv import load_dotenv

# Load environment variables from file .env, stored in this directory.
load_dotenv()


class Config:
    """Set Flask configuration from .env file."""

    # Flask configuration
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    SECRET_KEY = environ.get('SECRET_KEY')

    # Database configuration
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REPOSITORY = environ.get('REPOSITORY')

