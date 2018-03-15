import flask_login

class User(flask_login.UserMixin):

    @classmethod
    def get(self, user_id):
        if user_id == 'admin':
            user = User()
            user.id = user_id
            return user

        return None