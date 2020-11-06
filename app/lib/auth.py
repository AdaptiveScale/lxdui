from app.lib import conf
from app import __metadata__ as meta
import os
import json
import hashlib
import logging
import pam
import grp
import pwd

log = logging.getLogger(__name__)


class User(object):
    """
    User Management & Authentication Module
    """
    def __init__(self):
        try:
            self.auth_file = conf.Config().get(meta.APP_NAME, '{}.auth.conf'.format(meta.APP_NAME.lower()))
            self.users = self.load()
        except Exception('Unable to load configuration.') as e:
            log.debug(e)

        if self.users is None:
            print('Please initialize {} first.  e.g: {} init '.format(meta.APP_NAME, meta.APP_CLI_CMD))
            exit()

    def load(self):
        try:
            with open(self.auth_file, 'r') as f:
                # make sure the file is not empty
                if os.stat(self.auth_file).st_size != 0:
                    log.info('Reading auth file.')
                    data = f.read()
                    return json.loads(data)
        except (FileNotFoundError, IOError) as e:
            log.info('Unable to open auth file: ' + self.auth_file)
            log.debug(e)

    def save(self, data):
        try:
            with open(self.auth_file, 'w') as f:
                log.info('Saving auth file: {}'.format(self.auth_file))
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
        admin = conf.Config().get(meta.APP_NAME, '{}.admin.user'.format(meta.APP_NAME.lower()))

        if account is None:
            return err
            # raise Exception(err)

        # the admin user can't be deleted, panic!
        if username == admin:
            print('The admin user cannot be deleted.')
            exit(1)

        # remove the user from the list and save the new auth state
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
        try:
            pam_auth = conf.Config().get(meta.APP_NAME,'lxdui.pam')
            if pam_auth == 'true':
                if pam.authenticate(username,password):
                    try:
                        lxdui_group = conf.Config().get(meta.APP_NAME,'lxdui.group')

                        # get user groups
                        groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
                        gid = pwd.getpwnam(username).pw_gid
                        groups.append(grp.getgrgid(gid).gr_name)

                        for g in groups:
                            if g == lxdui_group:
                                return True, 'Authenticated'

                        return False, 'No required permissions.'
                    except:
                        # lxdui_group authentication was not chosen
                        return True, 'Authenticated'
                else:
                    return False, 'Incorrect password.'
            else:
                return self.authenticate_sha(username, password)
        except:
            # PAM authentication was not chosen
            return self.authenticate_sha(username, password)
        
    def authenticate_sha(self, username, password):
        account, err = self.get(username)

        if account is None:
            return 'Error', err

        if account['password'] == self.sha_password(password):
            return True, 'Authenticated'
        else:
            return False, 'Incorrect password.'
