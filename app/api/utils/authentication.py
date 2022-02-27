from app.lib.auth import User
from app.lib.conf import Config
from datetime import timedelta
from flask_jwt_extended import JWTManager

from app.api.utils import converters
import app.__metadata__ as meta
import logging
import secrets

logging = logging.getLogger(__name__)

def authenticate(username, password):
    logging.info("Authenticate user {}".format(username))
    if User().authenticate(username, password)[0] == True:
        logging.info("User {} successfully authenticated".format(username))
        return True
    else:
        logging.warning("Authentication failed for user {}".format(username))
        return False

def initAuth(app):
    APP = meta.APP_NAME
    tokenExpiration = int(Config().get(APP, '{}.jwt.token.expiration'.format(APP.lower())))
    # create a new secretKet whenever the system is started
    secretKey = secrets.token_urlsafe(32) 
    if (tokenExpiration == None):
        tokenExpiration = 1200

    tokenLocation = ["headers","cookies"]

    app.config['JWT_SECRET_KEY'] = secretKey
    app.config['JWT_TOKEN_LOCATION'] = tokenLocation
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=tokenExpiration)
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    jwt = JWTManager(app)
