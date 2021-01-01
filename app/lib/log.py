from app import __metadata__ as m
from app.lib.conf import MetaConf
from app.lib import conf
import os
import logging.handlers
import json
import logging
import logging.config

class Log:
    def __init__(self, __name__, log_config):
        conf.Config()
        self.configFile = log_config
        self.configure(__name__)

    def configure(self, __name__):
        logging.basicConfig()
        with open(self.configFile, "r") as fd:
            logConf = json.load(fd)
            logging.config.dictConfig(logConf)
        logging.getLogger('werkzeug').setLevel(logging.CRITICAL)
        logging.getLogger('requests').setLevel(logging.CRITICAL)