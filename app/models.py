from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    role = Column(String)


class Vehicles(Base):
    __tablename__ = 'vehicles'

    plate = Column(String, primary_key=True)
    owner_id = Column(Integer)
    color = Column(String)
    brand = Column(String)


class Infractions(Base):
    __tablename__ = 'infractions'

    infractor_id = Column(Integer, primary_key=True, index=True)
    vehicle_plate = Column(String)
    timestamp = Column(DateTime(timezone=True))
    comments = Column(String)
