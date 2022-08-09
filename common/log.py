# Copyright 2016, Vccloud
import os
import logging
from logging import handlers
from config import config

ENV = os.environ.get('ENV', 'development')
CONF = config[ENV]

MAP_LOGLEVEL = {'debug': logging.DEBUG,
                'warning': logging.WARNING,
                'info': logging.INFO,
                'critical': logging.CRITICAL,
                'error': logging.ERROR}


def setup_logging(name):
    logger = logging.getLogger(name)
    logger.setLevel(MAP_LOGLEVEL[CONF.LOG_LEVEL])

    # create the logging file handler
    FILEPATH = CONF.LOG_FILE
    fh = handlers.TimedRotatingFileHandler(FILEPATH,
                                           when='D', backupCount=30)
    formatter = logging.Formatter('%(asctime)s -'
                                  ' %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fh)
    return logger


if __name__ == "__main__":
    LOG = setup_logging(__name__)
    LOG.info("Welcome to  Logging")
    LOG.debug("A debugging message")
    LOG.warning("A warning occurred")
    LOG.error("An error occurred")
    LOG.exception("An Exception occurred")
