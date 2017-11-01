"""Request/Response Schemas are defined here"""
# pylint: disable=invalid-name

from marshmallow import Schema, fields, validate

from todo.constants import TO_DO, IN_PROGRESS, DONE


class TaskSchema(Schema):
    """Schema for serializing an instance of Task"""
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Str(
        required=True,
        validate=validate.OneOf(
            choices=[TO_DO, IN_PROGRESS, DONE],
            error="Status must be one of {choices} (given: {input})"))
    number = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)


class BoardSchema(Schema):
    """Schema for serializing an instance of Board"""
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)


class BoardDetailsSchema(BoardSchema):
    """Schema for serializing an instance of Board and its tasks"""
    tasks = fields.Nested(TaskSchema, many=True)
