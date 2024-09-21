from couchdb import Server
import couchdb
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

class CouchDB:
    load_dotenv()
    password = os.getenv("CouchDB_PASSWORD")
    def __init__(self, url=None):
        # Set default URL using the password from environment
        db_names = ["users", "posts" ]
        if url is None:
            url = f"http://admin:{self.password}@localhost:5984/"
        
        self.server = Server(url)       
        
        # Check if the database exists, otherwise create it
        for db_name in db_names:
            if db_name not in self.server:
                self.server.create(db_name)

        db_user = self.server['users']
        user_id_view.sync(db_user)
        auth_id_view.sync(db_user)


     # Create a document in the database
    def create_document(self, data, db_name):
        if '_id' not in data:
            data['_id'] = str(uuid.uuid4())
        if db_name in self.server:
            db = self.server[db_name]
        else:
            raise RuntimeError("Bad BD name")
        return db.save(data)

    # Read a document by its ID
    def read_documentId(self, doc_id, db_name):
        if db_name in self.server:
            db = self.server[db_name]
        else:
            raise RuntimeError("Bad BD name")
        try:
            return db[doc_id]
        except couchdb.http.ResourceNotFound:
            return None
    
    # Delete a document by its ID
    def delete_document(self, doc_id, db_name):
        if db_name in self.server:
            db = self.server[db_name]
        else:
            raise RuntimeError("Bad BD name")
        try:
            return db[doc_id].delete()
        except couchdb.http.ResourceNotFound:
            return None

    def read_user_id(self, user_id, db_name):
        if db_name in self.server:
            db = self.server[db_name]
        else:
            raise RuntimeError("Bad BD name")
        
        result = user_id_view(db)[user_id]
        # Collect and return all the documents related to the given user_id
        related_docs = [row.value for row in result]
        return related_docs

    def read_auth_id(self, auth_id, db_name):
        if db_name in self.server:
            db = self.server[db_name]
        else:
            raise RuntimeError("Bad BD name")
        
        result = auth_id_view(db)[auth_id]

        related_docs = [row.value for row in result]
        return related_docs