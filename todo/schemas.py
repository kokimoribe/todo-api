"""Request/Response Schemas are defined here"""
# pylint: disable=invalid-name

from marshmallow import Schema, fields


class TaskSchema(Schema):
    """Schema for api.portal.models.Panel"""
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
