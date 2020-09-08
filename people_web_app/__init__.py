from flask import Flask, request, url_for
from config import Config
import people_web_app.adapters.repository as repo
from people_web_app.domain.model import Person


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    with app.app_context():
        from .people_blueprint import people
        app.register_blueprint(people.people_blueprint)

    if test_config:
        app.config.from_mapping(test_config)
    repo.repo_instance = repo.PeopleRepository(
        Person(74633, 'Julius', 'Caeser'),
        Person(88337, 'Genghis', 'Khan'),
        Person(92731, 'Winston', 'Churchill'),
        Person(12826, 'Mahatma', 'Ghandi'),
        Person(92213, 'Nelson', 'Mandela')
    )
    return app
