import api.src.lib.log

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
