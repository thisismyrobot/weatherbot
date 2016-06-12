"""dnstwister web app."""
import flask

app = flask.Flask(__name__)
import views.index
