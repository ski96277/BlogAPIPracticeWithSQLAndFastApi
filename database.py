from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# set sqlite database path
SQLALCHEMY_DATABASE_URL = 'sqlite:///blog.db'

# create database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# create session with engine
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# create base
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()