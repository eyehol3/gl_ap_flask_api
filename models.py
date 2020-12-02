import os

from sqlalchemy import orm, UniqueConstraint
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import (
    Column, Integer, ForeignKey, String,
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


class Invited_users(BaseModel):
    __tablename__ = "invited_users"

    uid = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey(Events.uid))
    invited_user_uid = Column(Integer, ForeignKey(Users.uid))

    table_args = (UniqueConstraint('event_id', 'invited_user_id', name='invitation_un'),
                  )
    event = orm.relationship(Events, backref="events", lazy="joined")
    invited_user = orm.relationship(Users, backref="users", lazy="joined")



