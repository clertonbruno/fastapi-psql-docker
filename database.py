from os import environ as os_environ

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL = os_environ["DATABASE_URL"]

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Returns a database session.

    Yields:
        SessionLocal: The database session.

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
