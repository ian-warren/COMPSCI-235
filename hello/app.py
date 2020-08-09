from flask import Flask
from markupsafe import escape


app = Flask(__name__)


@app.route('/')
def index():
    return 'Index page'


@app.route('/hello')
def hello():
    return 'Hello, World!'


@app.route('/user/<username>')
def show_user_profile(username):
    # Show the user profile for that user
    return 'User %s' % escape(username)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # Show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # Show the subpath after /path/
    return 'Subpath %s' % escape(subpath)


@app.route('/news', methods=['GET'])
def shows_news():
    return "Today’s news is ..."
