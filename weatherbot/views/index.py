"""Index page."""
import flask

from weatherbot import app, cache, image, weather


@app.route(r'/')
def index():
    """Main page."""
    return flask.render_template('index.html')


@app.route('/radar_<int:index>.png')
@cache.memoize(300)
def radar_image(index):
    """Historical radar images."""
    assert 0 <= index <= 5
    return weather.get(index)


@app.route('/clouds_<int:index>.png')
@cache.memoize(300)
def clouds(index):
    """Return a PNG with cloudy sections highlighted."""
    img = radar_image(index)

    pil_img = image.data_to_pil(img)
    clouds_pil_img = image.clouds(pil_img)

    layered_pil_img = image.overlay(clouds_pil_img, pil_img)

    return image.pil_to_data(layered_pil_img)
