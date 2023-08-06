import logging
import logging.config

logging.config.dictConfig(
    {
        "version": 1,
        "filters": {
            "hooks_filter": {"name": "cookiecutter_python.hooks"},
            "backend_filter": {"name": "cookiecutter_python.backend"},
            "handle_filter": {"name": "cookiecutter_python.handle"},
        },
        "formatters": {
            "simple": {"format": "%(asctime)s - %(message)s", "datefmt": "%y%j-%H%M%S"},
            "detailed": {"format": "%(asctime)s - %(pathname):%(lineno) - %(message)s"},
        },
        "handlers": {
            "stderr": {
                "class": "logging.StreamHandler",
                "level": "WARNING",
                #   "filters": ["hooks_filter"],
                "formatter": "detailed",
                "stream": "ext://sys.stderr",
            },
            # "alert": {
            #   "class": "logging.handlers.SMTPHandler",
            #   "level": "ERROR",
            #   "formatter": "detailed",
            #   "mailhost": "smtp.skynet.com",
            #   "fromaddr": "logging@skynet.com",
            #   "toaddrs": [ "admin1@skynet.com", "admin2@skynet.com" ],
            #   "subject": "System Alert"
            # }
        },
        "loggers": {
            "cookiecutter_python": {"handlers": ["stderr", "alert"], "level": "ERROR"},
        },
    }
)
