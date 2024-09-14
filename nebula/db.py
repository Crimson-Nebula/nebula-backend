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
    def __init__(self, url="http://admin:" + password + "@localhost:5984/", db_name='test'):
        self.server = Server(url)
        self.db_name = db_name
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
        

if __name__ == "__main__":
    db = CouchDB()

    # Create a new document
    new_doc = {"name": "John Doe", "age": 30, "city": "New York"}
    db.create_document(new_doc)

    # Read the document
    doc_id = new_doc['_id']
    document = db.read_document(doc_id)
    print(document)