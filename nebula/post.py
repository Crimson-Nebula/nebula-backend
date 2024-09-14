import functools
from flask import jsonify

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
    #database.createPost(data)
    return 'OK', 200

