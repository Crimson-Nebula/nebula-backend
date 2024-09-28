import time
from flask import (
    Blueprint, Response, request, session, current_app, jsonify
)

bp = Blueprint('feed', __name__, url_prefix='/feed')

### HOW TO USE COUCHDB INSTANCE ###
# How to connect to database: couchdb_instance = current_app.config['COUCHDB_CONNECTION']
# You can use the functions of the CouchDB class from the instance, DO NOT need to use import statements
# Remember to check the return types :)
### END ###

@bp.before_request
def verify_session():
    #Respond to CORS preflight requests
    if request.method.lower() == 'options':
        return Response()

    #Enforce logged in
    if 'user_id' not in session:
        print("Not logged in")
        return "Not logged in", 401
    if time.time() > session['expiry']:
        print("Session Expired")
        return "Session Expired", 401

@bp.route('/', methods=['GET'])
def get_feed():
    db = current_app.config['COUCHDB_CONNECTION']

    documents = db.read_recent_posts(int(time.time()) - 60 * 60 * 24) #all posts in the past 24 hours

    posts = []
    for doc in documents:
        user = db.read_user_id(doc['posterId'], "users")[0]

        post = {
            "id": doc["post_id"],
            "content": doc["content"],
            "timestamp": doc["timestamp"],
            "posterId": doc["posterId"],
            "username": user["username"],
        }
        posts.append(post)

    response = {
        "page": 0,
        "pagination": 0,
        "posts": posts
    }

    return jsonify(response)
