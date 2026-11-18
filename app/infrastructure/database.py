import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DEBUG = os.getenv("DEBUG", "False") == "True"

engine = create_engine(DATABASE_URL, echo=DEBUG) if DATABASE_URL else None


# Create configured session class
SessionLocal = sessionmaker(bind=engine) if engine is not None else None

# Create base class for all models
Base = declarative_base()


def get_db():
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL must be configured to use the database.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
