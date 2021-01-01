from app import __metadata__ as meta
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path
from shutil import copy
import os
import io
import logging
log = logging.getLogger(__name__)
APP = meta.APP_NAME

'''
This component is responsible for configuration management.

If this is the first time the app is run then it will create the  
config file, and set the system environment variables for the app

The logic for checking the existence of the conf file
and creating it if it's missing should be in init.py 

TODO:
    Add 2 more config sources
    1) service - Get config from a service endpoint (JSON)
    2) db - Get config from a database
'''
class MetaConf(object):
    def __init__(self):
        conf = ConfigParser()
        conf.read_string(meta.__default_config__)
        self.defaultConfig = conf
        self.resolveMacros()
        self.config_file = self.getConfPaths()

    def resolveMacros(self):
        for section in self.defaultConfig.sections():
            for k in self.defaultConfig.options(section):
                v = self.defaultConfig.get(section, k)
                if '{{app_root}}' in v:
                    v = v.replace('{{app_root}}', self.getAppRoot())

                    self.defaultConfig.set(section, k, v)

    def getAppRoot(self):
        # First try the environment
        app_root=os.environ.get("APP_ROOT")
        if app_root:
            return app_root

        # If not env set, use a relative path
        module_dir = os.path.dirname(__file__)
        app_dir = os.path.dirname(module_dir)
        return os.path.dirname(app_dir)


    def getConfPaths(self):
        # default locations for the config files
        config_file = os.path.join(self.getAppRoot(), "conf","lxdui.conf")

        if os.environ.get("CONF_FILE"):
            config_file = os.environ.get("CONF_FILE")

        return config_file

class Config(object):

    def __init__(self, **kwargs):
        """
        Initialises the Config object and loads the configuration into memory.

          Order of operations:
            1) if a config file has been provided then use that one
            2) check to see if we have a local config file, and if so use that
            3) no config file found so we'll create one with defaults

        :param kwargs: conf=</path/to/config/file> #External source
        """
        m = MetaConf()

        self.config = None
        self.config_file = m.config_file

        if Path(self.config_file).exists():
            log.info('Using config file path = {}'.format(self.config_file))
            self.config = self.load('ini', self.config_file)
        # load the default config from meta
        elif meta.AUTO_LOAD_CONFIG:
            print("file doesnt exists:", self.config_file)
            log.info('Load default config (meta)')
            self.config = m.defaultConfig
            self.save()
        else:
            raise Exception('Unable to load the configuration.')

    def load(self, conf_type, *file_path):
        """
        Load the configuration into memory.
        The configuration is stored in the Config object.

        :param conf_type:
        :param file_path:
        :return:
        """
        if conf_type == 'external':
            external_conf_file = Path(*file_path)
            config = self.getConfig(external_conf_file)
            return config
        elif conf_type == 'ini':
            conf = self.getConfig(self.config_file)
            return conf
        elif conf_type == 'service':
            raise Exception('Not implemented.')
        elif conf_type == 'db':
            raise Exception('Not implemented.')
        else:
            raise Exception('Unable to determine configuration type.')

    def get(self, section, key):
        """
        Retrieve a configuration parameter.

        :param section: The section of the ini file to search
        :param key: The key to look up
        :return: Returns the value associated with the key
        """
        return self.config.get(section, key)

    def set(self, section, key, value):
        """
        Update a configuration parameter.

        :param section: The section of the ini config file to update
        :param key: The key that needs to be updated
        :param value: The new value associated with the key
        :return:
        """
        self.config.set(section, key, value)

    def show(self):
        """
        Prints out a listing of the config file to the console.

        :return:
        """
        for section in self.config.sections():
            for k in self.config.options(section):
                v = self.config.get(section, k)
                print('{} = {}'.format(k, v))

    def save(self):
        """
        Save the contents of the config object to the conf file.

        :return:
        """
        with open(self.config_file, 'w') as f:
            self.config.write(f)


    def getConfig(self, file):
        """
        Checks to ensure that the file exists Retrieves the contents of the config file.

        :param file: A string representing the path to the conf file.
        :return: Returns a config object.
        """
        # if the file exists then read the contents
        if Path(file).exists():
            try:
                config = self.parseConfig(file)
                return config
            except IOError as e:
                log.info('Unable to open file.', e)
        else:
            raise FileNotFoundError

    @staticmethod
    def parseConfig(file):
        """
        Parses the config file.  The file must be of ini format.
        If the file exists but is empty and exception will be generated.

        :param file: The path of the file to parse
        :return: Return a config object
        """
        # make sure the file is not empty
        size = Path(file).stat().st_size
        if size != 0:
            config = ConfigParser(interpolation=ExtendedInterpolation())
            config.read(file.__str__())
            return config
        else:
            raise Exception('File is empty.')