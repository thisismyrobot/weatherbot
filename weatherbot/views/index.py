"""Index page."""
import flask

from weatherbot import app


@app.route(r'/')
def index():
    """Main page."""
    return flask.render_template('index.html')
