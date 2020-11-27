import os

from sqlalchemy import orm
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
)

DB_URI = os.getenv("DB_URI", "postgres://postgres:dagger@localhost:5432/postgres")
engine = create_engine(DB_URI)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

BaseModel = declarative_base()


class Users(BaseModel):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True)
    name = Column(String)


class Events(BaseModel):
    __tablename__ = "events"

    uid = Column(Integer, primary_key=True)
    name = Column(String)
    datetime = Column(String)
    owner_uid = Column(Integer, ForeignKey(Users.uid))

    owner = orm.relationship(Users, backref="events", lazy="joined")