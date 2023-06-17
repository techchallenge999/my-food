from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


postgres_db = config('POSTGRES_DB')
postgres_user = config('POSTGRES_USER')
postgres_password = config('POSTGRES_PASSWORD')

sqlalchemy_database_url = f'postgresql://{postgres_user}:{postgres_password}@{postgres_db}:5432/db'
engine = create_engine(sqlalchemy_database_url)


Base.metadata.create_all(engine)
