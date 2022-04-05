from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:pass@localhost:54320/db_test"

engine = create_engine(DATABASE_URL)
#  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#  Base = declarative_base()


from databases import Database

async_db = Database(DATABASE_URL)
