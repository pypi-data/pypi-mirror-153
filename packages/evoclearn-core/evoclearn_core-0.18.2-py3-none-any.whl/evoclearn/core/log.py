# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers
from logging import getLogger


LOG_DIR = os.getenv("EVOCLEARN_LOG_DIR")
LOG_LEVEL = os.getenv("EVOCLEARN_LOG_LEVEL") or logging.INFO


def setup_logger(logname, log_dir=LOG_DIR, log_level=LOG_LEVEL):
    loglevel = int(LOG_LEVEL)
    fmt = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    logger = logging.getLogger(logname)
    formatter = logging.Formatter(fmt)
    # Always log to stderr:
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.setLevel(loglevel)
    # Possibly log to a log_dir
    if log_dir is not None:
        logfname = os.path.join(LOG_DIR, logname + ".log")
        ofstream = logging.handlers.TimedRotatingFileHandler(logfname,
                                                             when="D",
                                                             interval=1,
                                                             encoding="utf-8")
        ofstream.setFormatter(formatter)
        logger.addHandler(ofstream)
    return logger


LOGGER = setup_logger("evl")
