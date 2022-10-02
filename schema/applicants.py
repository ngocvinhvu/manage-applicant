from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models.applicants import Countries, Status


class ApplicantSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String()
    email = fields.String()
    dob = fields.DateTime()
    country = fields.String()
    status = EnumField(Status)
    created_dttm = fields.DateTime()
    identifify_number = fields.Integer()
    phone_number = fields.Integer()
    permanent_residence = fields.String()
    nationality = EnumField(Countries)
    new_applicant = fields.Boolean()
    place = fields.String()


class AppllicantPostSchema(ApplicantSchema):
    dob = fields.String()


class ApplicantOut(Schema):
    applicant_id = fields.UUID()
    status = fields.String()
