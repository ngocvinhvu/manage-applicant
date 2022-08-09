import os
from enum import Enum, unique
from config import config
from sqlalchemy import desc, DateTime
from sqlalchemy.sql import func
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


class Applicant(CommonModel):
    __tablename__ = "applicant"

    name = db.Column(db.String)
    email = db.Column(db.String)
    dob = db.Column(DateTime(timezone=True), server_default=func.now())
    country = db.Column(pgEnum(Countries))
    status = db.Column(db.String, default="pending")

    def __init__(self, name, email, dob, country, status):
        self.name = name
        self.email = email
        self.dob = dob
        self.status = "pending"
        self.country = country
        self.status = status


class ApplicantService(object):
    @classmethod
    def find_all_applicants(cls, items_per_page=None, page=None):
        filtered_machines = Applicant.query.order_by(desc(Applicant.created_dttm))
        if items_per_page and page:
            machines = (
                filtered_machines.offset(items_per_page * (page - 1))
                .limit(items_per_page)
                .all()
            )
        else:
            machines = filtered_machines.all()
        return machines, filtered_machines.count()

    @classmethod
    def find_by_id(cls, applicant_id):
        if not is_valid_uuid(applicant_id):
            raise ApplicantNotFoundException()

        applicant = Applicant.query.filter(Applicant.id == applicant_id).first()
        if not applicant:
            raise ApplicantNotFoundException(
                message=f"Machine {applicant_id} could not be found "
            )
        return applicant
