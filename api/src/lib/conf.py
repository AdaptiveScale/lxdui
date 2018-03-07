import __metadata__ as meta
import configparser
import os
import pathlib
import logging
log = logging.getLogger(__name__)

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
        log_path = self.getAbsPath(meta.LOG_DIR, meta.LOG_FILE)
        ini_path = self.getAbsPath(meta.CONF_DIR, meta.CONF_FILE)

        # conf file specified by the caller
        if kwargs:
            file = kwargs.get('conf')
            log.info('Loading external config file: {}'.format(file))
            if file:
                self.conf_path = file
                self.config = self.load('external', self.conf_path)
                self.envSet(log=log_path, conf=ini_path)
            else:
                raise Exception('Unsupported parameter {}'.format(kwargs))
        # no conf parameters specified so check local conf file
        elif pathlib.Path(ini_path).exists():
            log.info('Using ini config file path = {}'.format(ini_path))
            self.conf_path = ini_path
            self.config = self.load('ini', self.conf_path)
            self.envSet()
        # load the default config from meta
        elif meta.AUTO_LOAD_CONFIG:
            log.info('Load default config (meta)')
            self.envSet()
            self.conf_path = self.envGet().get('LXDUI_CONF')
            self.config = self.load('meta', self.conf_path)
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
            conf_file_path = pathlib.Path(*file_path)
            config = self.getConfig(conf_file_path)
            return config
        elif conf_type == 'ini':
            conf_source = os.path.join(meta.CONF_DIR, meta.CONF_FILE)
            conf_path = os.path.abspath(conf_source)
            conf_file_path = pathlib.Path(conf_path)
            actual_path = self.findConf(conf_file_path, conf_source)
            log.debug('actual_path = {}'.format(actual_path))
            conf = configparser.ConfigParser()
            conf.read(actual_path)
            return conf
        elif conf_type == 'meta':
            conf = configparser.ConfigParser()
            conf.read_string(meta.__default_config__)
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
        with open(self.conf_path, 'w') as f:
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
            log_path = self.getAbsPath(meta.LOG_DIR, meta.LOG_FILE)
            conf_path = self.getAbsPath(meta.CONF_DIR, meta.CONF_FILE)

        os.environ['{}_LOG'.format(meta.APP_NAME)] = log_path
        os.environ['{}_CONF'.format(meta.APP_NAME)] = conf_path

    def envShow(self):
        if not self.envGet():
            print('Environment variables for {} have not been set'.format(meta.APP_NAME))
        else:
            for k, v in self.envGet().items():
                print('{} = {}'.format(k, v))

    def getAbsPath(self, dir, file):
        """
        Retrieve the absolute path of a given directory and a file contained within.

        :param dir: The directory resolved to an absolute path
        :param file: File name
        :return: Returns a string representing the full path
        """
        path = os.path.join(os.path.abspath(dir), file)
        return path

    def getConfig(self, file):
        """
        Retrieves the contents of the config file.  Checks to ensure
        that the file exists and that is not

        :param file: A string representing the path to the conf file.
        :return: Returns a config object.
        """
        # if the file exists then read the contents
        if file.exists():
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
        size = file.stat().st_size
        if size != 0:
            config = configparser.ConfigParser()
            config.read(file.__str__())
            return config
        else:
            raise Exception('File is empty.')

    @staticmethod
    def findConf(conf_file_path, conf_source):
        """
        Check if the file exists.  It will search the parents up the path
        tree to find a match.

        :param conf_file_path:
        :param conf_source:
        :return: Return a string representing the path
        """
        for dir in conf_file_path.parents:
            file = os.path.join(dir.__str__(), conf_source)
            if pathlib.Path(file).exists():
                return file
            else:
                raise FileNotFoundError