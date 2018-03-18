import json
import configparser
import hashlib
import os
import logging
from pathlib import Path
from OpenSSL import crypto
from socket import gethostname

CONF_FILE = '../../conf/lxdui.conf'  # lxdui.conf.dir
APP_NAME = 'LXDUI'  # lxdui.app.alias
LOG_DIR = '/Users/vetoni/PycharmProjects/lui-cli/logs'



logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    filename=LOG_DIR + '/lxdui.log',
                    # filename='logs/' + __name__ + '.log',
                    filemode='w')
# write INFO messages or higher to the sys.stderr
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
sh.setFormatter(formatter)
# add the handler to the logger
log = logging.getLogger(__name__)
log.addHandler(sh)

class Init(object):
    """

    Generate an auth file and the client certificates to initialize the app

    If there is no auth file create it with the provided admin user password
    - If there is an auth file from a previous configuration, prompt the user that
      it will be overwritten
    - The admin username is specified in the conf file

    If this is the first time LXDUI is run then there should be no client certificates
    - Check if there are certs from a previous config
    - Generate the client certificates is they don't exist and prompt the user to
      overwrite if they do exit

    If the config file does not exit or has not been provided by the user,
     then create


    """

    def __init__(self, password):
        c = Config()
        self.password = User.sha_password(password)
        self.username = c.get(APP_NAME, 'lxdui.admin.user')
        self.auth_file = c.get(APP_NAME, 'lxdui.auth.conf')
        self.cert_file = c.get(APP_NAME, 'lxdui.ssl.cert')
        self.key_file = c.get(APP_NAME, 'lxdui.ssl.key')
        self.key, self.cert = Certificate.create()
        self.account = [{'username': self.username, 'password': self.password}]
        log.debug('Initializing auth file with: username = {}, password = {}'
                 .format(self.username, self.password))
        self.create('auth', self.auth_file)
        self.create('key', self.key_file)
        self.create('cert', self.cert_file)
        print('LXDUI is now configured.  You can now use '
              'the admin account to log in to the app.')

    def create(self, file_type, file_path):
        fod = Path(file_path)
        if fod.exists():
            if fod.is_file():
                if os.stat(file_path).st_size != 0:
                    print('File already exists: {}'.format(file_path))
                    self.replace(file_type, file_path)
                else:
                    print("File already exists, but it's empty: {} .".format(file_path))
                    self.create_file(file_type)
            else:
                print('Filename {} is a directory!'.format(file_path))
                raise Exception('{} is a directory!'.format(file_path))
        else:
            self.create_file(file_type)

    def replace(self, file_type, file_path):
        # prompt the user if the file should be deleted
        reply = input("Do you want to delete it and create a new one? [[y]/n] ")
        if reply == 'y' or reply == '':
            os.remove(file_path)
            self.create_file(file_type)
        else:
            print("Aborting...")
            exit()

    def create_file(self, file_type):
        if file_type == 'auth':
            User.save(self.account)

        if file_type == 'key':
            Certificate.save(self.key)

        if file_type == 'cert':
            Certificate.save(self.cert)


class User(object):
    def __init__(self):
        try:
            self.auth_file = Config().get(APP_NAME, 'lxdui.auth.conf')
            self.users = self.load()
        except Exception('Unable to load configuration.') as e:
            log.debug(e)

        if self.users is None:
            print('Please initialize {} first.  e.g: lui init '.format(APP_NAME))
            exit()

    def load(self):
        try:
            with open(self.auth_file, 'r') as f:
                # make sure the file is not empty
                if os.stat(self.auth_file).st_size != 0:
                    # log.info('Reading auth file.')
                    data = f.read()
                    return json.loads(data)
        except (FileNotFoundError, IOError) as e:
            log.debug('Unable to open auth file: ' + self.auth_file)
            log.debug(e)

    def save(self, data):
        try:
            with open(self.auth_file, 'w') as f:
                # log.info('Saving auth file: {}'.format(AUTH_FILE))
                f.write(json.dumps(data, indent=2))
        except (FileNotFoundError, IOError) as e:
            log.info('Unable to open file for writing.')
            log.debug(e)

    def get(self, username):
        users = []
        account = None

        for user in self.users:
            # create a list of user names for validation
            users.append(user['username'])
            # store the dictionary object to delete
            if user['username'] == username:
                account = user

        if username not in users:
            return None, 'User "{}" does not exist.'.format(username)
        else:
            return account, None

    @classmethod
    def sha_password(cls, password):
        sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        return sha1_password

    def show(self):
        # retrieve just the user names
        counter = 0
        for user in self.users:
            username = user['username']
            counter += 1
            print('{}. {}'.format(counter, username))

    def add(self, username, password):
        # check if the user exists first
        for user in self.users:
            if user['username'] == username:
                print('User "{}" already exists.'.format(user['username']))
                # raise Exception('Duplicate user name')
                exit()

        data = self.users
        sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        data.append({'username': username, 'password': sha1_password})
        self.save(data)

    def delete(self, username):
        account, err = self.get(username)
        admin = Config().get('LXDUI', 'lxdui.admin.user')

        if account is None:
            return err
            # raise Exception(err)

        # the admin user can't be deleted, panic!
        if username == admin:
            print('The admin user cannot be deleted.')
            exit(1)

        # remove the user from the list and safe the new auth state
        else:
            self.users.remove(account)
            print('User "{}" has been deleted.'.format(username))
            self.save(self.users)

    def update(self, username, password):
        # change password
        account, err = self.get(username)

        if account is None:
            return err

        account['password'] = self.sha_password(password)
        self.users.remove(account)
        self.users.append(account)
        # save the new auth state when done
        self.save(self.users)

    def authenticate(self, username, password):
        account, err = self.get(username)

        if account is None:
            return 'Error', err

        if account['password'] == self.sha_password(password):
            return True, 'Authenticated'
        else:
            return False, 'Incorrect password.'


class Config(object):
    def __init__(self):
        self.config = self.load()

    @classmethod
    def load(cls):
        try:
            config_path = os.getcwd() + '/' + CONF_FILE
            # make sure the file is not empty
            if os.stat(config_path).st_size != 0:
                conf = configparser.ConfigParser()
                conf.read(config_path)
                log.debug('Config file loaded: ' + config_path)

                return conf
        except (FileNotFoundError, IOError) as e:
            log.info('Unable to open file.')
            log.info(e)
            exit()

    def get(self, section, key):
        return self.config.get(section, key)

    def set(self, section, key, value):
        self.config.set(section, key, value)

    def show(self):
        for section in self.config.sections():
            for option in self.config.options(section):
                print(option, '=', self.config.get(section, option))

    def save(self):
        with open(CONF_FILE, 'w') as f:
            self.config.write(f)


class Certificate(object):

    def __init__(self):
        self.auth_file = Config().get(APP_NAME, 'lxdui.auth.conf')
        self.cert_file = Config().get(APP_NAME, 'lxdui.ssl.cert')
        self.key, self.cert = self.create()

    # Create a self signed certificate
    @staticmethod
    def create():
        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 1024)

        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = "US"
        cert.get_subject().ST = "Texas"
        cert.get_subject().L = "Dallas"
        cert.get_subject().O = "AdaptiveScale, Inc."
        cert.get_subject().OU = "OU=AdaptiveScale, DN=com"
        cert.get_subject().CN = gethostname()
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha1')

        key = crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
        cert = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)

        return key, cert

    @staticmethod
    def save(file, data):
        try:
            with open(file, 'wb') as f:
                f.write(data)
        except (FileNotFoundError, IOError) as e:
            log.info('Unable to open file.')
            log.info(e)