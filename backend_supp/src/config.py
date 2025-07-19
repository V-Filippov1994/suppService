import os
from starlette.config import Config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = Config(os.path.join(BASE_DIR, '.env'))

DB_USER = config("POSTGRES_USER")
DB_PASSWORD = config("POSTGRES_PASSWORD")
DB_HOST = config("DB_HOST")
DB_PORT = config("POSTGRES_PORT")
DB_NAME = config("POSTGRES_DB")


db_uri = f"{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}@{config('DB_HOST')}:{config('POSTGRES_PORT')}/{config('POSTGRES_DB')}"
DATABASE_URL = f"postgresql://{db_uri}"
DATABASE_URL_ASYNC = f"postgresql+asyncpg://{db_uri}"
