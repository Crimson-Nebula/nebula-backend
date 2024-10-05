import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from . import user, post, feed
from .db import CouchDB


def create_app(test_config=None):
    load_dotenv()
    secret = os.getenv("SECRET_KEY")
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = secret
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = True
    CORS(app, supports_credentials=True)

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
    app.register_blueprint(post.bp)
    app.register_blueprint(feed.bp)
    return app


