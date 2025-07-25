from marshmallow import EXCLUDE, Schema, fields


class UserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    # basic fields
    id = fields.Int(required=True)
    email = fields.Email(allow_none=True)
    image = fields.Str(allow_none=True)
    emailVerified = fields.DateTime(allow_none=True)
    name = fields.Str(allow_none=True)
    phone_number = fields.Str(allow_none=True)
    pin_number = fields.Str(allow_none=True)
    password_hash = fields.Str(allow_none=True)
    created_at = fields.DateTime(required=True)
    last_updated = fields.DateTime(required=True)


class PostSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    title = fields.Str(required=True)
    body = fields.Str(required=True)
    deleted = fields.Bool(required=True)
    created_at = fields.DateTime(required=True)
    last_updated = fields.DateTime(required=True)
    user = fields.Nested(UserSchema, dump_only=True)
