import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Load the hidden variables from the .env file
load_dotenv()

# Fetch the URL securely (No passwords in this file!)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Helper to provide database sessions to our routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()