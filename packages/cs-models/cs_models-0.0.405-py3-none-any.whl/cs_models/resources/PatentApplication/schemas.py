from marshmallow import (
    Schema,
    fields,
    validate,
    pre_load,
)

from ...utils.utils import pre_load_date_fields


class PatentApplicationResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    application_number = fields.String(required=True)
    jurisdiction = fields.String(required=True)
    app_grp_art_number = fields.Integer(allow_none=True)
    abstract_text = fields.String(allow_none=True)
    filed_date = fields.DateTime(allow_none=True)
    inventors = fields.String(allow_none=True)
    applicant = fields.String(allow_none=True)
    title = fields.String(allow_none=True)
    app_class = fields.String(allow_none=True)
    app_sub_class = fields.String(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)

    @pre_load
    def convert_string_to_datetime(self, in_data, **kwargs):
        date_fields = [
            'filed_date',
        ]
        in_data = pre_load_date_fields(
            in_data,
            date_fields,
            date_format='%Y/%m/%d',
        )
        return in_data


class PatentApplicationQueryParamsSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer()
    application_number = fields.String(validate=not_blank)
    jurisdiction = fields.String(validate=not_blank)
