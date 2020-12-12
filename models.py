import os

from sqlalchemy import orm, UniqueConstraint
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import app
from sqlalchemy import (
    Column, Integer, ForeignKey, String,
)



# BaseModel = declarative_base()

BaseModel = app.db.Model
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



# app.db.create_all()
