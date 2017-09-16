#DRINI FLASK_LOGIN
import flask_login
from flask import redirect, url_for, flash, current_app


class User(flask_login.UserMixin):
    pass

#flask-login
login_manager = flask_login.LoginManager()

@login_manager.user_loader
def user_loader(username):
    if username != current_app.config["LXDUI_USERNAME"]:
        return
    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username != current_app.config["LXDUI_USERNAME"]:
        return

    user = User()
    user.id = username

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = (current_app.config["LXDUI_PASSWORD"] == request.form['password'])
    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    flash('Authentication required !','info')
    return redirect(url_for('home'))
