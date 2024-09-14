import functools
from flask import jsonify

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, current_app
)

bp = Blueprint('user', __name__, url_prefix='/user')

### HOW TO USE COUCHDB INSTANCE ###
# How to connect to database: couchdb_instance = current_app.config['COUCHDB_CONNECTION']
# You can use the functions of the CouchDB class from the instance, DO NOT need to use import statements
# Remember to check the return types :)
### END ###

@bp.route('/create', methods=['POST'])
def register():
    return jsonify({"status": "Not Implemented"})

@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        print(request.cookies)
        print(request.form)

    return jsonify({'response': 'success'})

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = ""

@bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view