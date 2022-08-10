import os
import logging
from config import config

from flask_cors import CORS
from flask_restful import Api
from flask import Flask
from flask_migrate import Migrate
from flask_script import Manager
from raven.contrib.flask import Sentry

from resources.business.healcheck import HealthCheckResource
from resources.business.applicants import ApplicantResource, ApplicantIdResource
from resources.business.results import ResultResource


ENV = os.environ.get("ENV", "development")
CONF = config[ENV]

migrate = Migrate()
manager = Manager()
sentry = Sentry()


def create_app():
    app = Flask(__name__)
    app.config.from_object(CONF)
    app.config.from_pyfile("config.py")

    if CONF.ENABLE_CORS:
        CORS(
            app,
            origins=CONF.CORS_ALLOW_ORIGINS,
            methods=CONF.CORS_ALLOW_METHODS,
            expose_headers=CONF.CORS_EXPOSE_HEADERS,
            allow_headers=CONF.CORS_ALLOW_HEADERS,
            supports_credentials=CONF.CORS_ALLOW_CREDENTIALS,
            max_age=CONF.CORS_MAX_AGE,
        )

    from models import db

    db.init_app(app)
    migrate.init_app(app, db)
    sentry.init_app(app, dsn=CONF.SENTRY_DSN, logging=True, level=logging.ERROR)
    api = Api(app)

    api.add_resource(HealthCheckResource, "/healthcheck")
    api.add_resource(ApplicantResource, "/applicants")
    api.add_resource(ApplicantIdResource, "/applicants/<applicant_id>")
    api.add_resource(ResultResource, "/process")

    return app
