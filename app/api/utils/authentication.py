import jwt

from app.lib.auth import User
from app.lib.conf import Config
from datetime import timedelta
from flask_jwt import JWT
from app.api.utils import converters
import app.__metadata__ as meta
import logging

logging = logging.getLogger(__name__)

def authenticate(username, password):
    logging.info("Authenticate user {}".format(username))
    if User().authenticate(username, password)[0] == True:
        logging.info("User {} successfully authenticated".format(username))
        return converters.json2obj('{"id": 1, "username": "'+username+'", "password": "'+password+'"}')
    else:
        logging.warning("Authentication failed for user {}".format(username))
        return False


def identity(payload):
    return payload


def initAuth(app, config):
    APP = meta.APP_NAME
    tokenExpiration = int(config.get(APP, '{}.jwt.token.expiration'.format(APP.lower())))
    secretKey = config.get(APP, '{}.jwt.secret.key'.format(APP.lower()))
    authUrlRule = config.get(APP, '{}.jwt.auth.url.rule'.format(APP.lower()))
    if (tokenExpiration == None):
        tokenExpiration = 1200

    app.config['SECRET_KEY'] = secretKey
    app.config['JWT_AUTH_URL_RULE'] = authUrlRule
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=tokenExpiration)
    JWT(app, authenticate, identity)

def jwt_decode_handler(token):
    try:
        APP = meta.APP_NAME
        secretKey = Config().get(APP, '{}.jwt.secret.key'.format(APP.lower()))
        payload = jwt.decode(token, secretKey, algorithm='HS256')
        return True
    except jwt.InvalidTokenError:
        return False
