import __metadata__
import configparser
import os
import pathlib
import logging
log = logging.getLogger(__name__)

# if this is the first time the app is run then create the config file
# set the system environment variables for the app


class Config(object):
    def __init__(self, **conf_file):
        # self.conf_path = os.getcwd() + '/conf/' + __metadata__.CONF_FILE
        if conf_file:
            self.conf_path = conf_file
        else:
            self.conf_path = __metadata__.CONF_FILE
        self.config = self.load()
        # conf_dir = os.path.expanduser(os.path.join('~'))

    def load(self):
        log.info('Loading: ' + self.conf_path)
        path = pathlib.Path(self.conf_path)
        if path.exists():
            try:
                # make sure the file is not empty
                if os.stat(self.conf_path).st_size != 0:
                    conf = configparser.ConfigParser()
                    conf.read(self.conf_path)
                    log.debug('Config file loaded: ' + self.conf_path)

                    return conf
            except (FileNotFoundError, IOError) as e:
                log.info('Unable to open file.')
                log.info(e)
                exit()
        else:
            print(__metadata__.__default_config__)

    def get(self, section, key):
        return self.config.get(section, key)

    def set(self, section, key, value):
        self.config.set(section, key, value)

    def show(self):
        for section in self.config.sections():
            for option in self.config.options(section):
                print(option, '=', self.config.get(section, option))

    def save(self):
        with open(self.conf_path, 'w') as f:
            self.config.write(f)

    def checkFile(self):

        pass

    def checkEnv(self):
        # if environment variables have not been set then set them
        for k, v in __metadata__:
            os.environ["k"] = v

    def showEnv(self):
        # if environment variables have not been set then set them
        for k, v in __metadata__:
            print(v)