import logging
import os

from rasa.utils.redactor import Redactor
import json_logging

from rasa import version

# define the version before the other imports since these need it
__version__ = version.__version__

from rasa.run import run
from rasa.train import train
from rasa.test import test
from rasa.constants import (
    ENV_ENABLE_JSON_LOGGING,
    ENV_LOG_LEVEL
)

if ENV_ENABLE_JSON_LOGGING:
    json_logging.init_non_web(enable_json=True)
    LOG_LEVEL = ENV_LOG_LEVEL
    logging.basicConfig(level=LOG_LEVEL)
    json_logging.config_root_logger()

logging.getLogger(__name__).addHandler(logging.NullHandler())


class RedactingFilter(logging.Filter):

    def __init__(self):
        super(RedactingFilter, self).__init__()
        self.redactor = Redactor()

    def filter(self, record):
        record.msg = self.redact(record.msg)
        if isinstance(record.args, dict):
            for k in record.args.keys():
                record.args[k] = self.redact(record.args[k])
        else:
            record.args = tuple(self.redact(arg) for arg in record.args)
        return True

    def redact(self, msg):
        msg = self.redactor.redact_string_strict(str(msg))
        return msg


logging.getLogger().addFilter(RedactingFilter())
