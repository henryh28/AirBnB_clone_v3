#!/usr/bin/python3
""" API definition """

from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(code):
    """ Closes storage """
    storage.close()


@app.errorhandler(404)
def code_404(error):
    """
       Ref: http://flask.pocoo.org/docs/0.12/patterns/errorpages/
       https://kite.com/docs/python;flask.helpers.make_response
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", "5000"))
    app.run(host, port)
