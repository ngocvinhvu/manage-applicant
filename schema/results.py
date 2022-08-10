from enum import unique, Enum

from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from models.applicants import Status


class ProcessResults(Schema):
    applicant_id = fields.UUID(required=True)
    client_key = fields.String()
    applicant_status = EnumField(Status)
    processed_dttm = fields.DateTime()
