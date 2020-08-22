from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return 'Homepage'

    @app.route('/greet/<name>')
    def say_hello(name: str):
        return render_template('hello.html', name=name)

    @app.route('/people')
    def list_people():
        list_of_people = ['Mohandas Gandhi', 'Nelson Mandela', 'Martin Luther King', 'Abraham Lincoln',
                          'George Washington', 'Napolean Bonaparte', 'Franklin Roosevelt', 'Winston Churchill']
        return render_template('people.html', people=list_of_people)

    @app.route('/<name>')
    def make_html_page(name: str):
        return render_template(name + '.html', message='Hello!')

    return app
