from marshmallow import Schema, fields

class ExamSchema(Schema):
    id = fields.Number()
    value = fields.Str()
    description = fields.Str()
    order = fields.Number()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
