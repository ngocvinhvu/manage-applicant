from enum import Enum, unique
from flask import abort
from email_validator import validate_email, EmailNotValidError
from datetime import datetime
from sqlalchemy import desc, DateTime
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from common import http_status_code
from models import db, is_valid_uuid
from models.common_model import CommonModel
from exceptions import ApplicantNotFoundException


@unique
class Countries(Enum):
    VIETNAM = "VIETNAM"
    SINGAPORE = "SINGAPORE"
    LAOS = "LAOS"
    INDONESIA = "INDONESIA"
    THAILAND = "THAILAND"
    CAMPUCHIA = "CAMPUCHIA"
    MALAYSIA = "MALAYSIA"


@unique
class Status(Enum):
    processed = "processed"
    pending = "pending"
    failed = "failed"


def verify_dob(dob):
    try:
        date_of_birth = datetime.strptime(dob, "%Y/%m/%d")
        return date_of_birth
    except ValueError:
        abort(
            http_status_code.HTTP_400_BAD_REQUEST,
            "Date of birt is invalid must id Year/month/day",
        )


def verify_email(email):
    try:
        email = validate_email(email).email
        return email
    except EmailNotValidError as e:
        abort(http_status_code.HTTP_400_BAD_REQUEST, str(e))


class Applicants(CommonModel):
    __tablename__ = "applicants"

    name = db.Column(db.String)
    identify_number = db.Column(db.BigInteger)
    phone_number = db.Column(db.BigInteger)
    email = db.Column(db.String)
    dob = db.Column(DateTime)
    country = db.Column(db.String)
    permanent_residence = db.Column(db.String)
    nationality = db.Column(pgEnum(Countries))
    status = db.Column(pgEnum(Status), default=Status.pending)
    new_applicant = db.Column(db.Boolean)
    place = db.Column(db.String)

    def __init__(
        self, name, email, dob, country, permanent_residence, nationality, new_applicant, identify_number, phone_number, place
    ):
        self.name = name
        self.email = email
        self.dob = dob
        self.country = country
        self.permanent_residence = permanent_residence
        self.nationality = nationality
        self.new_applicant = new_applicant
        self.identify_number = identify_number
        self.phone_number = phone_number
        self.place = place

class ApplicantService(object):
    @classmethod
    def find_all_applicants(cls, items_per_page=None, page=None):
        filtered_applicants = Applicants.query.order_by(desc(Applicants.created_dttm))
        if items_per_page and page:
            applicants = (
                filtered_applicants.offset(items_per_page * (page - 1))
                .limit(items_per_page)
                .all()
            )
        else:
            applicants = filtered_applicants.all()
        return applicants, filtered_applicants.count()

    @classmethod
    def find_by_id(cls, applicant_id):
        if not is_valid_uuid(applicant_id):
            raise ApplicantNotFoundException()

        applicant = Applicants.query.filter(Applicants.id == applicant_id).first()
        if not applicant:
            raise ApplicantNotFoundException(
                message=f"Applicant {applicant_id} could not be found "
            )
        return applicant
