import os
import ast
from dotenv import load_dotenv
from pathlib import Path


basedir = os.path.abspath(os.path.dirname(__file__))
env_path = Path(".", ".env")


def _get_env_or_default(var_name, default_val):
    load_dotenv(env_path)
    return os.environ.get(var_name) or default_val


class BaseConfig(object):
    # LOG
    LANGUAGES = ["en", "vi"]
    DEBUG = _get_env_or_default("DEBUG", False)
    LOG_LEVEL = _get_env_or_default("LOG_LEVEL", "debug")
    LOG_FILE = _get_env_or_default("LOG_FILE", "/tmp/applicant-api.log")
    LOG_OPTION = _get_env_or_default("LOG_OPTION", "console")

    # Database
    SQLALCHEMY_DATABASE_URI = _get_env_or_default(
        "SQLALCHEMY_DATABASE_URI",
        "",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = _get_env_or_default(
        "SQLALCHEMY_TRACK_MODIFICATIONS", False
    )

    # Sentry
    SENTRY_DSN = _get_env_or_default("SENTRY_DSN", "")

    # CORS
    ENABLE_CORS = (
        True if _get_env_or_default("ENABLE_CORS", "true").lower() != "false" else False
    )
    CORS_ALLOW_ORIGINS = ast.literal_eval(
        _get_env_or_default("CORS_ALLOW_ORIGINS", "['*']")
    )
    CORS_ALLOW_METHODS = ast.literal_eval(
        _get_env_or_default(
            "CORS_ALLOW_METHODS",
            "['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE']",
        )
    )
    CORS_ALLOW_HEADERS = ast.literal_eval(
        _get_env_or_default("CORS_ALLOW_HEADERS", "['*']")
    )
    CORS_EXPOSE_HEADERS = ast.literal_eval(
        _get_env_or_default("CORS_EXPOSE_HEADERS", "['*']")
    )
    CORS_ALLOW_CREDENTIALS = (
        True
        if _get_env_or_default("CORS_ALLOW_CREDENTIALS", "true").lower() != "false"
        else False
    )
    CORS_MAX_AGE = None


class DevelopConfig(BaseConfig):
    pass


config = {"development": DevelopConfig}
