from marshmallow import Schema, fields, validate

class Credentials(Schema):
    username = fields.String()
    password = fields.String()

class UserData(Schema):
    uid = fields.Integer()
    name = fields.String()

class EventData(Schema):
    uid = fields.Integer()
    name = fields.String()
    datetime = fields.DateTime()
    description = fields.String()
    created_by = fields.Nested(UserData())

