from enum import unique, Enum

from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models.applicants import Countries, Status


class ApplicantSchema(Schema):
    id = fields.UUID()
    name = fields.String()
    email = fields.String()
    dob = fields.DateTime()
    country = EnumField(Countries)
    status = EnumField(Status)
    created_dttm = fields.DateTime()


class ApplicantOut(Schema):
    applicant_id = fields.UUID()
    status = fields.String()
