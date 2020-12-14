import os
import datetime
from sqlalchemy import orm, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import app
from sqlalchemy import (
    Column, Integer, ForeignKey, String, DateTime
)



# app.db.Model = declarative_base()

# BaseModel = app.db.Model
class Users(app.db.Model):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, )

    UniqueConstraint(name)

    def __init__(self, name, uid=None):
        self.name = name
        self.uid = uid
class Events(app.db.Model):
    __tablename__ = "events"

    uid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    datetime = Column(DateTime, default=datetime.datetime.now)
    description = Column(String)
    owner_uid = Column(Integer, ForeignKey(Users.uid))

    owner = orm.relationship(Users, backref="events", lazy="joined")

    def __init__(self, name, description, uid=None, datetime=None, owner_uid=None, invited_users=None):
        self.name = name
        self.description = description
        self.uid = uid
        self.datetime = datetime
        self.owner_uid = owner_uid


class Invited_users(app.db.Model):
    __tablename__ = "invited_users"

    # uid = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey(Events.uid))
    invited_user_uid = Column(Integer, ForeignKey(Users.uid))

    table_args = (UniqueConstraint('event_id', 'invited_user_id', name='invitation_un'),
                  )
    event = orm.relationship(Events, backref="events", lazy="joined")
    invited_user = orm.relationship(Users, backref="users", lazy="joined")
    
    __table_args__ = (PrimaryKeyConstraint(event_id, invited_user_uid),)
app.db.create_all()
