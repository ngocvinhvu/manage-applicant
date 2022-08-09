import os
from config import config

from flask_cors import CORS
from flask_restful import Api
from flask import Flask
from flask_migrate import Migrate
from flask_script import Manager

from resources.business.healcheck import HealthCheckResource


ENV = os.environ.get("ENV", "development")
CONF = config[ENV]

migrate = Migrate()
manager = Manager()


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
    api = Api(app)

    api.add_resource(HealthCheckResource, "/healthcheck")
    return app
