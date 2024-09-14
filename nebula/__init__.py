import os

from flask import Flask, jsonify
from flask_cors import CORS
from . import user
from .db import CouchDB


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    # Connecting to the database
    # Creating a instance of the class to connect, 
    # Here the instance of the connection is made directly as it is under the __init__ function of the class
    couchdb_instance = CouchDB()
    app.config['COUCHDB_CONNECTION'] = couchdb_instance


    # a simple page that says hello
    @app.route('/')
    def hello():
        return jsonify({"Hello": "World"})

    app.register_blueprint(user.bp)
    return app
