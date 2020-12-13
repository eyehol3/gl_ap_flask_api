from marshmallow import Schema, fields, validate, post_load
from models import Users, Events
class Credentials(Schema):
    username = fields.String()
    password = fields.String()

class UserData(Schema):
    uid = fields.Integer()
    name = fields.String()

    @post_load
    def make_user(self, data, **kwargs):
        return Users(**data)
class EventData(Schema):
    uid = fields.Integer()
    name = fields.String()
    datetime = fields.DateTime()
    description = fields.String()
    created_by = fields.Nested(UserData())
    invited_users = fields.List(fields.Integer)

    @post_load
    def make_event(self, data, **kwargs):
        return Events(**data)
    