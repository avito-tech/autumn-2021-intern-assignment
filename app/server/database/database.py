from sqlalchemy import create_engine,String,DateTime,Column,Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  sessionmaker
from sqlalchemy_utils import database_exists, create_database

from config import DB_PASSWORD, DB_NAME


database_url = f"postgresql+psycopg2://postgres:{DB_PASSWORD}@localhost/{DB_NAME}"
engine=create_engine(database_url)

Session = sessionmaker(engine)
Base = declarative_base()

if not database_exists(engine.url):
    create_database(engine.url)


class Users(Base):
    __tablename__ = 'Users'




class Transactions(Base):
    __tablename__ = 'Transactions'