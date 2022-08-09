from enum import unique, Enum

from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models.applicants import Countries


class Applicants(Schema):
    id = fields.UUID()
    name = fields.String()
    email = fields.String()
    dob = fields.DateTime()
    country = EnumField(Countries)
    status = fields.String()


class ApplicantOut(Schema):
    applicant_id = fields.UUID()
    status = fields.String()


class ProcessResults(Schema):
    applicant_id = fields.UUID()
    client_key = fields.String()
    applicant_status = fields.String()