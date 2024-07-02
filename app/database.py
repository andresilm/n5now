from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DB_URL = 'sqlite:///registries.db'

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

