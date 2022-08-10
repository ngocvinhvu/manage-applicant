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


ENV = os.environ.get("ENV", "development")
CONF = config[ENV]


def model_onupdate_listener(mapper, connection, instance):
    instance.created_at = instance.created_at
    if instance.status == Status.processed:
        instance.processed_dttm = UtcNow()


def generate_key(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(letters_and_digits) for i in range(length)))


class Results(CommonModel):
    __tablename__ = "results"

    status = db.Column(pgEnum(Status), default=Status.pending)
    applicant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('applicant.id'), nullable=False)
    applicant = relationship('Applicants')
    processed_dttm = db.Column(DateTime(), server_default=UtcNow())

    def __init__(self, applicant_id, status):
        self.applicant_id = applicant_id
        self.status = status


event.listen(CommonModel, 'before_update', model_onupdate_listener, propagate=True)
