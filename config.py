import os
import ast
from dotenv import load_dotenv
from pathlib import Path


basedir = os.path.abspath(os.path.dirname(__file__))
env_path = Path('.', '.env')

def _get_env_or_default(var_name, default_val):
    load_dotenv(env_path)
    return os.environ.get(var_name) or default_val


class BaseConfig(object):
    LANGUAGES = ['en', 'vi']
    DEBUG = _get_env_or_default('DEBUG', False)
    LOG_LEVEL = _get_env_or_default('LOG_LEVEL', 'debug')
    LOG_FILE = _get_env_or_default('LOG_FILE', '/tmp/backup-api.log')
    LOG_OPTION = _get_env_or_default('LOG_OPTION', 'console')
    # Database
    SQLALCHEMY_DATABASE_URI = _get_env_or_default('SQLALCHEMY_DATABASE_URI',
                                                  'postgresql+psycopg2://postgres:vccloud123@10.3.54.111:5432/vinh-api')
    SQLALCHEMY_TRACK_MODIFICATIONS = _get_env_or_default('SQLALCHEMY_TRACK_MODIFICATIONS', False)


class DevelopConfig(BaseConfig):
    pass


config = {
    'development': DevelopConfig
}