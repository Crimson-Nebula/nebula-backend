import os
import time
import uuid

from flask import jsonify, Response
from google.oauth2 import id_token
from google.auth.transport import requests

from flask import (
    Blueprint, request, session, current_app
)

bp = Blueprint('user', __name__, url_prefix='/user')

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

    # Don't enforce auth on login endpoint
    if request.endpoint == "user.login":
        return None

    # Only require auth_id on signup endpoint
    if request.endpoint == "user.signup":
        if 'auth_id' not in session:
            return "No auth provided", 401
        else:
            return None

    #Enforce logged in
    if 'user_id' not in session:
        print("Not logged in")
        return "Not logged in", 401
    if time.time() > session['expiry']:
        print("Session Expired")
        return "Session Expired", 401

@bp.route('/signup', methods=['POST'])
def signup():
    db = current_app.config['COUCHDB_CONNECTION']

    user = {
        'user_id': str(uuid.uuid4()),
        'auth_id': session['auth_id'],
        'username': request.json['username']
    }

    db.create_document(user, "users")

    return "Success", 200

@bp.route('/login', methods=['POST'])
def login():
    try:
        token = request.form.get("credential")

        idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.getenv('GOOGLE_CLIENT_ID'))
        google_id = idinfo['sub']

        #Create session
        session['auth_id'] = google_id
        session['expiry'] = int(time.time()) + 3600 #Expires in 1 hour (for now)

        #Check if user exists
        db = current_app.config['COUCHDB_CONNECTION']

        user_lookup = db.read_auth_id(google_id, "users")
        print(user_lookup)

        user_exists = len(user_lookup) > 0
        if user_exists:
            #Redirect to home page
            session['user_id'] = user_lookup[0]['user_id']
            return jsonify({"status": "OK"})
        else:
            #Redirect to user creation page
            return jsonify({"status": "CREATE_USER"})

    except Exception as e:
        print(e)
        return "Failed to login", 500

@bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return "OK", 200