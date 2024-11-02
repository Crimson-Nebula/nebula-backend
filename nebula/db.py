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

DATABASE_URL = ""
if os.getenv("DOCKER") == "TRUE":
    print("Running in Docker")
    DATABASE_URL = f"postgresql://{username}:{password}@nebula_db/{db_name}"
else:
    print("Running directly on localhost")
    DATABASE_URL = f"postgresql://{username}:{password}@localhost/{db_name}"

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
    timestamp = Column(Integer)
    content = Column(String)
    externalUrl = Column(String)
    poster_id = Column(String)


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