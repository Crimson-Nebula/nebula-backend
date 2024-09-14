import os
import functools
import time
from flask import jsonify, Response
from google.oauth2 import id_token
from google.auth.transport import requests

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, current_app
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

    #Enforce logged in
    if 'user_id' not in session:
        print("Not logged in")
        return "Not logged in", 401
    if time.time() > session['expiry']:
        print("Session Expired")
        return "Session Expired", 401

@bp.route('/create', methods=['POST'])
def create():
    return jsonify({"status": "Not Implemented"})

@bp.route('/login', methods=['POST'])
def login():
    try:
        token = request.form.get("credential")

        idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.getenv('GOOGLE_CLIENT_ID'))
        google_id = idinfo['sub']

        #Create session
        session['user_id'] = google_id
        session['expiry'] = int(time.time()) + 60 #Expires in 1 minute

        #Check if user exists
        user_exists = False
        if user_exists:
            #Redirect to home page
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