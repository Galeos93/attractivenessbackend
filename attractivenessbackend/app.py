import flask
import os
from attractivenessbackend.routes import api

app = flask.Flask(__name__)
app.register_blueprint(api)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
os.environ["CUDA_VISIBLE_DEVICES"] = ""


@app.errorhandler(404)
def handle_404(e):
    return flask.jsonify(error=404, message=str(e)), 404
