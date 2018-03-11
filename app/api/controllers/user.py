from flask import Blueprint, request
from flask_login import login_user, logout_user
from app.api.core import login_manager
from app.api.utils import response
from app.api.schemas.userSchema import doValidate

from app.api.models.User import User

user_api = Blueprint('user_api', __name__)

@user_api.route('/login', methods=['POST'])
def login():
    input = request.get_json(silent=True)
    validation = doValidate(input)
    if validation:
        return response.replyFailed(message=validation.message)

    if input.get('username') == 'admin' and input.get('password') == 'admin':
        user = User()
        user.id = input.get('username')
        login_user(user)
        return response.replySuccess(message='Login Success')
    else:
        return response.replyFailed(message='Username or Password are incorect')

@user_api.route('/logout')
def logout():
    logout_user()
    return response.replySuccess(message='Logout Success')


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized_handler():
    return response.replyFailed(message='Unauthorized', status=401)