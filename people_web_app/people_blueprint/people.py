from flask import Blueprint, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired

import people_web_app.adapters.repository as repo

people_blueprint = Blueprint(
    'people_bp', __name__
)


@people_blueprint.route('/')
def home():
    return render_template(
        'home.html',
        find_person_url=url_for('people_bp.find_person'),
        list_people_url=url_for('people_bp.list_people')
    )


@people_blueprint.route('/list')
def list_people():
    pass


@people_blueprint.route('/find', methods=['GET', 'POST'])
def find_person():
    pass



