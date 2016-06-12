"""Index page."""
import flask

from weatherbot import app, cache, weather


@app.route(r'/')
def index():
    """Main page."""
    return flask.render_template('index.html')


@app.route('/latest.png')
@cache.memoize(300)
def latest():
    """The latest image."""
    return weather.get()
