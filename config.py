from os import environ, path, getenv
from dotenv import load_dotenv
load_dotenv()
class Config:
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get('SECRET_KEY')