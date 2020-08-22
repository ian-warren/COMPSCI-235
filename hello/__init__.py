from flask import Flask, render_template

# https://www.webforefront.com/django/createreusablejinjatemplates.html
# https://flask.palletsprojects.com/en/1.1.x/patterns/templateinheritance/
# https://en.wikipedia.org/wiki/Jinja_(template_engine)
# https://codeburst.io/jinja-2-explained-in-5-minutes-88548486834e
# https://realpython.com/primer-on-jinja-templating/#super-blocks

# https://alankent.me/2013/10/19/html-escaping-for-secure-web-pages/
# https: // portswigger.net / web - security / csrf / tokens
# https: // portswigger.net / web - security / csrf
# https: // en.wikipedia.org / wiki / Cross - site_scripting
# https: // flask.palletsprojects.com / en / 0.12.x / security /
# https: // owasp.org / www - community / attacks / xss /
# https: // jinja.palletsprojects.com / en / 2.11.x / templates /  #


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
