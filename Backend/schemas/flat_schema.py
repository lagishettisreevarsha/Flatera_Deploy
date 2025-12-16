from marshmallow import Schema, fields

class FlatSchema(Schema):
    flat_no = fields.String(required=True)
    bedrooms = fields.Integer(required=True)
    sqft = fields.Integer(required=True)
    rent = fields.Float(required=True)
    tower_id = fields.Integer(required=True)
    is_available = fields.Boolean(required=True)
