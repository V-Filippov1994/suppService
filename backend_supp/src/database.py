from typing import Any, AsyncGenerator

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine, text

from .config import DATABASE_URL, DATABASE_URL_ASYNC
from .mixins import BaseModelMixin

BaseModel = declarative_base(cls=BaseModelMixin)

engine = create_async_engine(DATABASE_URL_ASYNC, poolclass=NullPool, isolation_level='AUTOCOMMIT')
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def init_db():
    *db_url, db_name = DATABASE_URL.split('/')
    db_postgres = f'{"/".join(db_url)}/postgres'

    try:
        db_engine = create_engine(DATABASE_URL)
        with db_engine.connect():
            print(f'Database "{db_name}" already exists.')
    except OperationalError:
        print(f'Database "{db_name}" does not exist. Creating now.')
        db_engine = create_engine(db_postgres)
        with db_engine.connect() as conn:
            conn.execute(text(f'CREATE DATABASE {db_name};'))


async def get_async_session() -> AsyncGenerator[Any, Any]:
    async with async_session_maker() as session:
        yield session
