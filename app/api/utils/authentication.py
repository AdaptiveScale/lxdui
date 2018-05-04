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
    tokenExpiration = int(Config().get(APP, '{}.jwt.token.expiration'.format(APP.lower())))
    secretKey = Config().get(APP, '{}.jwt.secret.key'.format(APP.lower()))
    authUrlRule = Config().get(APP, '{}.jwt.auth.url.rule'.format(APP.lower()))
    if (tokenExpiration == None):
        tokenExpiration = 1200

    app.config['SECRET_KEY'] = secretKey
    app.config['JWT_AUTH_URL_RULE'] = authUrlRule
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=tokenExpiration)
    JWT(app, authenticate, identity)
