import time
from couchdb import Server
import uuid
from couchdb import Server
from flask import current_app, g
import os
from dotenv import load_dotenv
from couchdb.design import ViewDefinition

user_id_view = ViewDefinition(
    'users',   
    'by_user_id',  
    '''function (doc) {
        if (doc.user_id) {
            emit(doc.user_id, doc);
        }
    }'''
)
auth_id_view = ViewDefinition(
    'users',   
    'by_auth_id',  
    '''function (doc) {
        if (doc.auth_id) {
            emit(doc.auth_id, doc);
        }
    }'''
)

post_id_view = ViewDefinition(
    'posts',   
    'by_post_id',  
    '''function (doc) {
        if (doc.post_id) {
            emit(doc.post_id, doc);
        }
    }'''
)

post_timestamp_view = ViewDefinition(
    'posts',
    'by_post_timestamp',
    '''function (doc) {
        if (doc.timestamp) {
            emit(doc.timestamp, doc);
        }
    }'''
)


class CouchDB:
    load_dotenv()
    password = os.getenv("CouchDB_PASSWORD")
    def __init__(self, url=None):
        # Set default URL using the password from environment
        db_names = ["users", "posts" ]
        if url is None:
            if os.getenv("DOCKER") == "TRUE":
                print("Running in Docker")
                url = f"http://admin:{self.password}@nebula_db:5984/"
            else:
                print("Running directly on localhost")
                url = f"http://admin:{self.password}@localhost:5984/"
        print("Connected to DB")

        self.server = Server(url)       
        
        # Check if the database exists, otherwise create it
        db_connected = False

        while not db_connected:
            print("Attempting to connect to DB")
            try:
                for db_name in db_names:
                    if db_name not in self.server:
                        self.server.create(db_name)
                db_connected = True
            except Exception as e:
                time.sleep(1)

        db_user = self.server['users']
        db_post = self.server['posts']
        user_id_view.sync(db_user)
        auth_id_view.sync(db_user)
        post_id_view.sync(db_post)
        post_timestamp_view.sync(db_post)

     # Create a document in the database
    def create_user_document(self, data):
        if '_id' not in data:
            data['_id'] = str(uuid.uuid4())
        if "users" in self.server:
            db = self.server["users"]
        else:
            raise RuntimeError("Bad DB name")
        return db.save(data)

    def create_post_document(self, data):
        if '_id' not in data:
            data['_id'] = str(uuid.uuid4())
        if "posts" in self.server:
            db = self.server["posts"]
        else:
            raise RuntimeError("Bad DB name")
        return db.save(data)
    

    def read_user_id(self, user_id):
        if "users" in self.server:
            db = self.server["users"]
        else:
            raise RuntimeError("Bad DB name")
        
        result = user_id_view(db)[user_id]
        # Collect and return all the documents related to the given user_id
        related_docs = [row.value for row in result]
        return related_docs[0]

    def read_auth_id(self, auth_id):
        if "users" in self.server:
            db = self.server["users"]
        else:
            raise RuntimeError("Bad DB name")
        
        result = auth_id_view(db)[auth_id]

        related_docs = [row.value for row in result]
        return related_docs  
    
    def read_posts_all(self, post_id):
        if "posts" in self.server:
            db = self.server["posts"]
        else:
            raise RuntimeError("Bad DB name")
        result = post_id_view(db)[post_id]
        # Collect and return all the documents related to the given user_id
        related_docs = [row.value for row in result]
        return related_docs


    #All posts made after the time_cutoff (unix time) will be returned
    def read_recent_posts(self, time_cutoff):
        db = self.server['posts']
        result = post_timestamp_view(db)[time_cutoff:]
        # Collect and return all the documents that matched
        related_docs = [row.value for row in result]
        return related_docs