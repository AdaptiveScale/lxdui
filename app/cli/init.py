from app.lib import conf, auth, cert
from pathlib import Path
from app import __metadata__ as meta
import shutil
import os
import logging
log = logging.getLogger(__name__)

class Init(object):
    """

    Init is intended to be run once after installation of the app.
    Its responsibility is to create the requisite files that the
    app will use to operate properly.

    Re-running init will reset the app's configuration to a clean state.
    Make sure to back up any previous configs!

    1) Create Log File

        By default we'll try to use a well known location for logs:
        /var/log/<app_name>/<app_name>.log

        If we don't have permission to write to /var/log we'll fall
        back to <app_root>/logs

    2) Create Conf File

        If the config file does not exit or has not been provided by the user:
        Create config file with:
        a) user provided path to the desired config file
            - use the config settings from that file
        b) default config settings from conf file

    3) Create Auth File

        If there is no auth file create it with the provided admin user password:
        a) If there is an auth file from a previous configuration, prompt the user that
          it will be overwritten
        b) The admin username is specified in the conf file

    4) Create Client Certs

        If this is the first time LXDUI is run then there should be no client certificates
        a) Check if there are certs from a previous config
        b) Generate the client certificates is they don't exist and prompt the user to
          overwrite if they do exit

    """

    APP = meta.APP_NAME

    def __init__(self, password):
        c = conf.Config()
        self.password = auth.User.bcrypt_password(password)
        self.username = c.get(self.APP, '{}.admin.user'.format(self.APP.lower()))
        self.auth_file = c.get(self.APP, '{}.auth.conf'.format(self.APP.lower()))
        self.cert_file = c.get(self.APP, '{}.ssl.cert'.format(self.APP.lower()))
        self.key_file = c.get(self.APP, '{}.ssl.key'.format(self.APP.lower()))
        self.key, self.cert = cert.Certificate().create()
        self.account = [{'username': self.username, 'password': self.password}]
        #self.create('auth', self.auth_file)
        #self.create('key', self.key_file)
        #self.create('cert', self.cert_file)
        log.debug('Initializing auth file with: username = {}, password = {}'.format(self.username, self.password))
        print('LXDUI is now configured.  You can now use '
              'the admin account to log in to the app.')

    def create(self, file_type, file_path):
        file = Path(file_path)
        if file.exists():
            if file.is_file():
                if file.stat() != 0:
                    print('File already exists: {}'.format(file_path))
                    self.replace(file_type, file_path)
                else:
                    print("File already exists, but it's empty: {} .".format(file_path))
                    self.createFile(file_type)
            else:
                print('Filename {} is a directory!'.format(file_path))
                raise Exception('{} is a directory!'.format(file_path))
        else:
            self.createFile(file_type)

    def replace(self, file_type, file_path):
        # prompt the user if the file should be deleted
        reply = input("Do you want to delete it and create a new one? [[y]/n] ")
        if reply == 'y' or reply == '':
            # os.rename(file_path, file_path + '.bak')
            os.remove(file_path)
            self.createFile(file_type)
        else:
            print("Aborting...")
            exit()

    def createConfig(self):
        # if the config file doesn't exist create it from the metadata
        pass

    def createFile(self, file_type):
        if file_type == 'auth':
            auth.User().save(self.account)

        if file_type == 'key':
            cert.Certificate().save(self.key)

        if file_type == 'cert':
            cert.Certificate().save(self.cert)

    def checkPrerequisites(self):
        '''
            Run a number of prerequisite checks to ensure that dependencies are available on the system
            - Python 3
            - LXD
        '''
        python3 = shutil.which('python3')
        lxd = shutil.which('lxd')


