import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from models import db
from sqlalchemy import (
    DateTime, event, func
)


def default_uuid():
    return str(uuid.uuid4())


class UtcNow(expression.FunctionElement):
    type = DateTime()


@compiles(UtcNow, 'postgresql')
def get_now(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


def model_oncreate_listener(mapper, connection, instance):
    instance.created_dttm = UtcNow()


# CommonModel
class CommonModel(db.Model):
    __abstract__ = True
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=default_uuid, server_default=func.uuid_generate_v4())
    created_dttm = db.Column(DateTime(), server_default=UtcNow())

    def create(self, resource):
        """
        Save resource to database
        resource is object for saving
        :param resource:
        :return:
        """
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        """
        Update resource
        """
        return db.session.commit()

    def delete(self):
        """
        Delete resource
        """
        self.deleted = True
        return db.session.commit()


event.listen(CommonModel, 'before_insert', model_oncreate_listener, propagate=True)
