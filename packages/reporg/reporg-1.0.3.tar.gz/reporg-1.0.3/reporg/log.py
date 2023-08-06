# Copyright (c) Vyoma Systems Private Limited
# See LICENSE.vyoma for details

import logging.config


logging_dict = {
    "version": 1,
    "disable_existing_loggers": True,  # set True to suppress existing loggers from other modules
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
        },
    },
    "formatters": {
        "colored_console": {
            "()": "coloredlogs.ColoredFormatter",
            "format": " %(name)s | %(message)s",
            "datefmt": "%H:%M:%S",
        },
        "format_for_file": {
            "format": "%(asctime)s : %(levelname)s : %(funcName)s in %(filename)s (l:%(lineno)d) | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "colored_console",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "format_for_file",
            "filename": "run.log",
            "maxBytes": 500000,
            "backupCount": 5,
        },
    },
}
logging.config.dictConfig(logging_dict)
logger = logging.getLogger(__name__)
