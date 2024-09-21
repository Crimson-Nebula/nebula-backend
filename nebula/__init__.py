import os

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from . import user
from .db import CouchDB


def create_app(test_config=None):
    load_dotenv()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = "dev"
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

    # Test data setup: Create new documents
    db_name = "users"
    new_doc1 = {"name": "John Doe", "auth_id": 1, "user_id": 1, "Post IDs": [1,2,5]}
    new_doc2 = {"name": "John Doe", "auth_id": 1, "user_id": 1, "Post ID": 21}
    couchdb_instance.create_document(new_doc1, db_name)
    couchdb_instance.create_document(new_doc2, db_name)

    test_related = couchdb_instance.read_auth_id(1, db_name)
    print(test_related)
    
    app.register_blueprint(user.bp)
    return app


