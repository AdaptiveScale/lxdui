from app.lib.auth import User
from app.lib.conf import Config
from datetime import timedelta
from flask_jwt import JWT
from app.api.utils import converters
import app.__metadata__ as meta

def authenticate(username, password):
    if User().authenticate(username, password)[0] == True:
        return converters.json2obj('{"id": 1, "username": "'+username+'", "password": "'+password+'"}')
    else:
        return False


def identity(payload):
    return payload


def initAuth(app):
    APP = meta.APP_NAME
    tokenExpiration = int(Config().get(APP, '{}.token.expiration'.format(APP.lower())))
    if (tokenExpiration == None):
        tokenExpiration = 1200

    app.config['SECRET_KEY'] = 'AC8d83&21Almnis710sds'
    app.config['JWT_AUTH_URL_RULE'] = '/api/user/login'
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=tokenExpiration)
    JWT(app, authenticate, identity)
