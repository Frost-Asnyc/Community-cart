from marshmallow import EXCLUDE, Schema, fields, validate


class ListingSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1))
    description = fields.String(required=True, validate=validate.Length(min=1))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    category = fields.String(required=True, validate=validate.Length(min=1))
    condition = fields.String(load_default=None)
    image_url = fields.String(load_default=None)
    location = fields.String(load_default=None)
    status = fields.String(dump_only=True)
    owner_id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
