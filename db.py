import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database


DATABASE_URL = os.environ.get("DATABASE_URL")
assert DATABASE_URL is not None

engine = create_engine(DATABASE_URL)
async_db = Database(DATABASE_URL)
