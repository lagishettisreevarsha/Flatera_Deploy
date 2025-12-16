from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=4))
    role = fields.Str(required=False, validate=validate.OneOf(['user', 'admin']))