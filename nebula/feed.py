import functools
from flask import jsonify
from datetime import datetime
import uuid


from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, current_app
)

bp = Blueprint('feed', __name__, url_prefix='/feed')

### HOW TO USE COUCHDB INSTANCE ###
# How to connect to database: couchdb_instance = current_app.config['COUCHDB_CONNECTION']
# You can use the functions of the CouchDB class from the instance, DO NOT need to use import statements
# Remember to check the return types :)
### END ###

@bp.route('/read', methods=['GET'])
def get_feed():
    db = current_app.config['COUCHDB_CONNECTION']
    db_name = "posts"

    ## TODO: Get all the posts from the posts database
    ## TODO: Sort the posts using their timestamps and return the most recent 5 posts
