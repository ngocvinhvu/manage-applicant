import os, random, string
from config import config
from sqlalchemy import DateTime, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from models import db
from models.common_model import CommonModel
from models.applicants import Status
from models.common_model import UtcNow
from datetime import date


ENV = os.environ.get("ENV", "development")
CONF = config[ENV]


def model_oncreate_listener(mapper, connection, instance):
    instance.processed_dttm = UtcNow()


def generate_key(length):
    letters_and_digits = string.ascii_letters + string.digits
    return "".join((random.choice(letters_and_digits) for i in range(length)))


def check_approve(dob):
    year = dob.strftime("%Y")
    month = dob.strftime("%m")
    day = dob.strftime("%d")
    curent_date = str(date.today())
    curent_year = curent_date.split("-")[0]
    curent_month = curent_date.split("-")[1]
    curent_day = curent_date.split("-")[2]
    if int(curent_year) - int(year) < 15:
        status = Status.failed
    elif int(curent_year) - int(year) == 15 and int(curent_month) < int(month):
        status = Status.failed
    elif int(curent_year) - int(year) == 15 and int(curent_month) == int(month) and int(curent_day) < int(day):
        status = Status.failed
    else:
        status = Status.processed

    return status


class Results(CommonModel):
    __tablename__ = "results"

    applicant_status = db.Column(pgEnum(Status), default=Status.pending)
    applicant_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("applicants.id"), nullable=False
    )
    client_key = db.Column(db.String)
    applicant = relationship("Applicants")
    processed_dttm = db.Column(DateTime(), server_default=UtcNow())

    def __init__(self, applicant_id, applicant_status, client_key):
        self.applicant_id = applicant_id
        self.applicant_status = applicant_status
        self.client_key = client_key


event.listen(Results, "before_insert", model_oncreate_listener, propagate=True)
