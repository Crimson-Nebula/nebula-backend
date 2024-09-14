from couchdb import Server
import couchdb
import uuid
from couchdb import Server
from flask import current_app, g
import os
from dotenv import load_dotenv


class CouchDB:
    load_dotenv()
    password = os.getenv("CouchDB_PASSWORD")
    def __init__(self, url=None, db_name='test'):
        # Set default URL using the password from environment
        if url is None:
            url = f"http://admin:{self.password}@localhost:5984/"
        
        self.server = Server(url)
        self.db_name = db_name
        
        # Check if the database exists, otherwise create it
        if db_name in self.server:
            self.db = self.server[db_name]
        else:
            self.db = self.server.create(db_name)

     # Create a document in the database
    def create_document(self, data):
        if '_id' not in data:
            data['_id'] = str(uuid.uuid4())
        return self.db.save(data)

    # Read a document by its ID
    def read_document(self, doc_id):
        try:
            return self.db[doc_id]
        except couchdb.http.ResourceNotFound:
            return None