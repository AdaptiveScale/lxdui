from app import __metadata__ as m
import os
import logging.handlers


class Log:
    def __init__(self, __name__):
        self.log = os.path.join(m.LOG_DIR, m.LOG_FILE)
        self.configure(__name__)

    def configure(self, __name__):
        logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] %(name)-12s.%(funcName)s - %(levelname)-8s:: %(message)s',
                        datefmt='%Y-%m-%d %H:%M.%S',
                        filename=self.log,
                        filemode='w')

        # write INFO messages or higher to the sys.stderr
        sh = logging.StreamHandler()
        # slh = logging.handlers.SysLogHandler(address='/dev/log')

        # set the logging level for the log handler(s)
        sh.setLevel(logging.INFO)
        # slh.setLevel(logging.INFO)

        # set the message format for the logger
        formatter = logging.Formatter('[%(asctime)s] %(name)-12s.%(funcName)s - %(levelname)-8s:: %(message)s')
        # formatter = logging.Formatter('%(name)-12s: %(levelname)-8s: %(message)s')
        sh.setFormatter(formatter)
        # slh.setFormatter(formatter)

        # add the handler to the logger
        log = logging.getLogger(__name__)
        log.addHandler(sh)
        # log.addHandler(slh)

