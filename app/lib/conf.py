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
        self.config = conf
        self.resolveMacros()
        self.log_file, self.config_file = self.getConfPaths()

    def resolveMacros(self):
        for section in self.config.sections():
            for k in self.config.options(section):
                v = self.config.get(section, k)
                if '{{app_root}}' in v:
                    if 'SNAP_USER_COMMON' in Config.envGet2('SNAP_USER_COMMON'):
                        v = v.replace('{{app_root}}', self.getSnapPath())
                    else:
                        v = v.replace('{{app_root}}', self.getConfRoot())

                    self.config.set(section, k, v)

    def getConfRoot(self):

        module_dir = os.path.dirname(__file__)
        app_dir = os.path.dirname(module_dir)
        return os.path.dirname(app_dir)


    def getSnapPath(self):
        if not os.path.exists(str(Path.home()) + '/conf'):
            os.makedirs(str(Path.home()) + '/conf')
            os.makedirs(str(Path.home()) + '/logs')
            Path(str(Path.home()) + '/logs/lxdui.log').touch()
            copy(self.getConfRoot() + '/conf/auth.conf', str(Path.home()) + '/conf')
            copy(self.getConfRoot() + '/conf/log.conf', str(Path.home()) + '/conf')

        return str(Path.home())


    def getConfPaths(self):
        f = io.StringIO()
        self.config.write(f)
        c = ConfigParser(interpolation=ExtendedInterpolation())
        f.seek(0)
        c.read_file(f)
        log_file = c.get(APP, '{}.log.file'.format(APP.lower()))
        config_file = c.get(APP, '{}.conf.file'.format(APP.lower()))
        return log_file, config_file

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
        self.log_file = m.log_file
        self.config_file = m.config_file

        # conf file specified by the caller
        if kwargs:
            file = kwargs.get('conf')
            log.info('Loading external config file: {}'.format(file))
            if file:
                self.config = self.load('external', file)
                self.envSet(log=self.log_file, conf=file)
            else:
                raise Exception('Unsupported parameter {}'.format(kwargs))
        # no conf parameters specified so check local conf file
        elif Path(self.config_file).exists():
            log.info('Using config file path = {}'.format(self.config_file))
            self.config = self.load('ini', self.config_file)
            self.envSet()
        # load the default config from meta
        elif meta.AUTO_LOAD_CONFIG:
            log.info('Load default config (meta)')
            self.config = m.config
            self.envSet()
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
        self.save()

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

    @staticmethod
    def envGet():
        """
        Retrieve the environment variables containing the log and conf paths.

        :return: Returns a dictionary containing the file paths
        """
        env = {}
        for k, v in os.environ.items():
            if k in ['LXDUI_LOG', 'LXDUI_CONF']:
                env.update({k: os.environ.get(k)})
        return env

    @staticmethod
    def envGet2(key):
        """
        Retrieve the environment variables containing the log and conf paths.

        :return: Returns a dictionary containing the file paths
        """
        env = {}
        for k, v in os.environ.items():
            if key == k:
                env.update({k: os.environ.get(k)})
        return env

    def envSet(self, **kwargs):
        """
        Set the environment variables for the log and the conf file

        :param kwargs: Specify log=<log_path> and cong=<conf_path>
        :return:
        """
        log_path = None
        conf_path = None

        if kwargs.get('log') and kwargs.get('conf'):
            log_path = kwargs.get('log')
            conf_path = kwargs.get('conf')
            log.debug('Setting environment variables')
        else:
            log_path = self.log_file
            conf_path = self.config_file

        os.environ['{}_LOG'.format(APP)] = log_path
        os.environ['{}_CONF'.format(APP)] = conf_path

    def envShow(self):
        if not self.envGet():
            print('Environment variables for {} have not been set'.format(APP))
        else:
            for k, v in self.envGet().items():
                print('{} = {}'.format(k, v))

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