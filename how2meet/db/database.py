#!/usr/bin/env python3
"""
Boilerplate code needed to connect to a database.

FastAPI tutorial: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-sqlalchemy-parts

"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# TODO: connect to postres instance from env
SQLALCHEMY_DATABASE_URL = os.getenv("DB_CONN", "sqlite:///./data.db")

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)  # Postgres db


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # Base class inherited in models.py to declare new tables


# Dependency
def get_db() -> Session:
    """
    Generate a database session and return it as a context manager.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
