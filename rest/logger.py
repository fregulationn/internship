# -*- coding: utf-8 -*-
"""
File Name：     logger
Author :       junjie.zhang
-------------------------------------------------
"""
import logging.config
from rest import settings

LOG_PATH = settings.LOG_PATH

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'loggers': {
        'file': {
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': False
        },
        'werkzeug': {
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': False
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'backupCount': 30,
            'filename': LOG_PATH,
            'formatter': 'verbose',
        }
    },
    'formatters': {
        'verbose': {
            'format':
                '%(asctime)s %(levelname)s:%(name)s:%(lineno)d: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    }
}


def init_logger():
    """Init logger instance."""
    logging.config.dictConfig(LOGGING_CONFIG)
