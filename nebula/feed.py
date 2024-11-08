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

## TODO: Make it so that the posts are sent in a ordered list or something 


@bp.before_request
# def verify_session():
#     #Respond to CORS preflight requests
#     if request.method.lower() == 'options':
#         return Response()

#     #Enforce logged in
#     if 'user_id' not in session:
#         return {"status": "Not logged in"}, 401
#     if time.time() > session['expiry']:
#         return {"status": "Session Expired"}, 401

@bp.route('/', methods=['GET'])
def get_feed():
    db = current_app.config['DB_CONNECTION']

    documents = db.get_recent_posts(int(time.time()) - 60 * 60 * 24) #all posts in the past 24 hours

    posts = []
    for doc in documents:
        user = db.get_user_by_user_id(doc.poster_id)

        post = {
            "id": doc.post_id,
            "content": doc.content,
            "timestamp": doc.timestamp,
            "posterId": doc.poster_id,
            "username": user.username,
        }
        posts.append(post)
    # Sorting through the list an making it so that the posts are in a descending order in terms of time of posting
    sorted_posts = sorted(posts, key=lambda post: post['timestamp'], reverse=True)
    response = {
        "page": 0,
        "pagination": 0,
        "posts": sorted_posts
    }

    return jsonify(response), 200
