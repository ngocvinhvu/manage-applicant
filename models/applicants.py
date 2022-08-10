import os
from enum import Enum, unique
from config import config
from sqlalchemy import desc, DateTime
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from models import db, is_valid_uuid
from models.common_model import CommonModel
from exceptions import ApplicantNotFoundException


ENV = os.environ.get("ENV", "development")
CONF = config[ENV]


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


class Applicants(CommonModel):
    __tablename__ = "applicants"

    name = db.Column(db.String)
    email = db.Column(db.String)
    dob = db.Column(DateTime)
    country = db.Column(pgEnum(Countries))
    status = db.Column(pgEnum(Status), default=Status.pending)

    def __init__(self, name, email, dob, country, status):
        self.name = name
        self.email = email
        self.dob = dob
        self.status = status
        self.country = country
        self.status = status


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
