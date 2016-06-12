"""Index page."""
import flask

from weatherbot import app, cache, image, weather


@app.route(r'/')
def index():
    """Main page."""
    return flask.render_template('index.html')


@app.route('/latest.png')
@cache.memoize(300)
def latest():
    """The latest image."""
    img = weather.get()
    return img


@app.route('/clouds.png')
def clouds():
    """Return a PNG with cloudy sections highlighted PNG."""
    img = latest()

    pil_img = image.data_to_pil(img)
    clouds_pil_img, cloud_map = image.clouds(pil_img)

    return image.pil_to_data(clouds_pil_img)
