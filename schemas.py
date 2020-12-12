from marshmallow import Schema, fields, validate

class Credentials(Schema):
    username = fields.String()
    password = fields.String()

class UserData(Schema):
    id = fields.Integer()
    name = fields.String()

class EventData(Schema):
    id = fields.Integer()
    name = fields.String()
    date = fields.DateTime()
    description = fields.String()
    created_by = fields.Nested(UserData())

