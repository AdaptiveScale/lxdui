from datetime import timedelta

from flask_jwt import JWT

from api.src.utils import converters

# TODO implement proper auth checking
def authenticate(username, password):
    if username == 'admin' and password == 'admin':
        return converters.json2obj('{"id": 1, "username": "admin", "password": "admin"}')


def identity(payload):
    return payload


def initAuth(app):
    # TODO move to config
    app.config['SECRET_KEY'] = 'AC8d83&21Almnis710sds'
    app.config['JWT_AUTH_URL_RULE'] = '/api/user/login'
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1200)
    JWT(app, authenticate, identity)
