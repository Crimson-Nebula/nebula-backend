import time
import uuid
from flask import current_app, g
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Integer, TIMESTAMP
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()
password = os.getenv("POSTGRES_PASSWORD")
username = os.getenv("POSTGRES_USER")
db_name = os.getenv("POSTGRES_DB")
host = "localhost"

DATABASE_URL = f"postgresql://{username}:{password}@{host}/{db_name}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, unique=True)
    auth_id = Column(String, unique=True)
    username = Column(String)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    post_id = Column(String, unique=True)
    timestamp = Column(TIMESTAMP)
    content = Column(String)

def init_db():
    Base.metadata.create_all(engine)


class Database:
    def __init__(self):
        self.session = Session()

    def create_user(self, user_data):
        try:
            user = User(**user_data)
            self.session.add(user)
            self.session.commit()
            return user
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Failed to create user: {e}")

    def create_post(self, post_data):
        try:
            post = Post(**post_data)
            self.session.add(post)
            self.session.commit()
            return post
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Failed to create post: {e}")

    def get_user_by_user_id(self, user_id):
        return self.session.query(User).filter_by(user_id=user_id).first()

    def get_user_by_auth_id(self, auth_id):
        return self.session.query(User).filter_by(auth_id=auth_id).all()

    def get_post_by_post_id(self, post_id):
        return self.session.query(Post).filter_by(post_id=post_id).all()

    def get_recent_posts(self, time_cutoff):
        return self.session.query(Post).filter(Post.timestamp >= time_cutoff).all()
# class CouchDB:
#     load_dotenv()
#     password = os.getenv("CouchDB_PASSWORD")
#     def __init__(self, url=None):
#         # Set default URL using the password from environment
#         db_names = ["users", "posts" ]
#         if url is None:
#             if os.getenv("DOCKER") == "TRUE":
#                 print("Running in Docker")
#                 url = f"http://admin:{self.password}@nebula_db:5984/"
#             else:
#                 print("Running directly on localhost")
#                 url = f"http://admin:{self.password}@localhost:5984/"
#         print("Connected to DB")

#         self.server = Server(url)       
        
#         # Check if the database exists, otherwise create it
#         db_connected = False

#         while not db_connected:
#             print("Attempting to connect to DB")
#             try:
#                 for db_name in db_names:
#                     if db_name not in self.server:
#                         self.server.create(db_name)
#                 db_connected = True
#             except Exception as e:
#                 time.sleep(1)

#         db_user = self.server['users']
#         db_post = self.server['posts']
#         user_id_view.sync(db_user)
#         auth_id_view.sync(db_user)
#         post_id_view.sync(db_post)
#         post_timestamp_view.sync(db_post)

#      # Create a document in the database
#     def create_user_document(self, data):
#         if '_id' not in data:
#             data['_id'] = str(uuid.uuid4())
#         if "users" in self.server:
#             db = self.server["users"]
#         else:
#             raise RuntimeError("Bad DB name")
#         return db.save(data)

#     def create_post_document(self, data):
#         if '_id' not in data:
#             data['_id'] = str(uuid.uuid4())
#         if "posts" in self.server:
#             db = self.server["posts"]
#         else:
#             raise RuntimeError("Bad DB name")
#         return db.save(data)
    

#     def read_user_id(self, user_id):
#         if "users" in self.server:
#             db = self.server["users"]
#         else:
#             raise RuntimeError("Bad DB name")
        
#         result = user_id_view(db)[user_id]
#         # Collect and return all the documents related to the given user_id
#         related_docs = [row.value for row in result]
#         return related_docs[0]

#     def read_auth_id(self, auth_id):
#         if "users" in self.server:
#             db = self.server["users"]
#         else:
#             raise RuntimeError("Bad DB name")
        
#         result = auth_id_view(db)[auth_id]

#         related_docs = [row.value for row in result]
#         return related_docs  
    
#     def read_posts_all(self, post_id):
#         if "posts" in self.server:
#             db = self.server["posts"]
#         else:
#             raise RuntimeError("Bad DB name")
#         result = post_id_view(db)[post_id]
#         # Collect and return all the documents related to the given user_id
#         related_docs = [row.value for row in result]
#         return related_docs


#     #All posts made after the time_cutoff (unix time) will be returned
#     def read_recent_posts(self, time_cutoff):
#         db = self.server['posts']
#         result = post_timestamp_view(db)[time_cutoff:]
#         # Collect and return all the documents that matched
#         related_docs = [row.value for row in result]
#         return related_docs