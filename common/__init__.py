import os
from config import config
from common.log import setup_logging
from loguru import logger


ENV = os.environ.get("ENV", "development")
CONF = config[ENV]


if CONF.LOG_OPTION == "console":
    LOG = logger
else:
    LOG = setup_logging(__name__)
