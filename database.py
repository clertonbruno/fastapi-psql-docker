from os import environ as os_environ

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL = os_environ["DATABASE_URL"]

engine = create_async_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_db():
    """
    Returns an async database session.

    Yields:
        SessionLocal: The database session.

    """
    async with SessionLocal() as session:
        yield session
