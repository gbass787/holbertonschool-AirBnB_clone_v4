#!/usr/bin/python3
""" returns status of an API """
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv  # to use environmental variables
from flask import jsonify
from werkzeug.exceptions import HTTPException  # to use errorhandler
from flask_cors import CORS


# instance app variable from flask class
app = Flask(__name__)
# registers the blueprint app_views for usage
app.register_blueprint(app_views)
# Cors(origin resource sharing):https://flask-cors.readthedocs.io/en/latest/
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(self):
    """removes the current sqlalchemy session"""
    storage.close()


@app.errorhandler(HTTPException)
def handle_exception(error):
    """uses errorhandler to display 404 error page"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    # return env variable if it exists
    # otherwise return second argument
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True, debug=True)
