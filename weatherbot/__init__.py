"""dnstwister web app."""
import flask
import flask_cache

app = flask.Flask(__name__)
cache = flask_cache.Cache(app, config={'CACHE_TYPE': 'simple'})

import views.index
