import functools
from flask import jsonify
import time
import uuid


from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, current_app
)

bp = Blueprint('post', __name__, url_prefix='/post')

### HOW TO USE COUCHDB INSTANCE ###
# How to connect to database: couchdb_instance = current_app.config['COUCHDB_CONNECTION']
# You can use the functions of the CouchDB class from the instance, DO NOT need to use import statements
# Remember to check the return types :)
### END ###

@bp.route('/create', methods=['POST'])
def create_post():
    
    data = request.get_json()
    if data is None:
        return 'bad request', 400
    
    db = current_app.config['COUCHDB_CONNECTION']
    db_name = "posts"
    post = {
        "post_id": str(uuid.uuid4()),
        "content": data.get("content"),
        "externalUrl": data.get("externalUrl"),
        "timestamp": int(time.time()),
        "posterId": session["user_id"]
    }
    db.create_document(post, db_name)
    #database.createPost(data)
    return 'Success', 200

