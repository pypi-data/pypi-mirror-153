from marshmallow import (
    Schema,
    fields,
    validate,
)


class ClaimResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    patent_id = fields.Integer()
    patent_application_id = fields.Integer(required=True)
    claim_number = fields.Integer(required=True)
    claim_text = fields.String(required=True, validate=not_blank)
    updated_at = fields.DateTime(dump_only=True)


class ClaimQueryParamsSchema(Schema):
    id = fields.Integer()
    patent_id = fields.Integer()
    patent_application_id = fields.Integer()
    claim_number = fields.Integer()


class ClaimPatchSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    claim_text = fields.String(validate=not_blank)
