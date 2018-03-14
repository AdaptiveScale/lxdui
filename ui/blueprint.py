from flask import Blueprint, render_template, redirect
from jinja2 import TemplateNotFound
from api.src.models.LXCContainer import LXDModule
from flask_login import login_required

uiPages = Blueprint('uiPages', __name__, template_folder='src/templates',
                    static_folder='src/static')

@uiPages.route('/')
def index():
    return render_template('login.html', currentpage='Login')

@uiPages.route('/containers')
# @login_required
def container():
    containers = LXDModule().listContainers()
    return render_template('containers.html', currentpage='Containers',
                           containers=containers, lxdui_current_version='2.0')

@uiPages.route('/profiles')
# @login_required
def profile():
    profiles = LXDModule().listProfiles()
    return render_template('profiles.html', currentpage='Profiles',
                           profiles=profiles, lxdui_current_version='2.0')
@uiPages.route('/network')
# @login_required
def network():
    network = LXDModule().listNetworks()
    return render_template('network.html', currentpage='Network',
                           network=network, lxdui_current_version='2.0')

@uiPages.route('/images')
# @login_required
def images():
    localImages = LXDModule().listLocalImages()
    remoteImages = LXDModule().listRemoteImages()
    return render_template('images.html', currentpage='Images',
                           localImages=localImages,
                           remoteImages=remoteImages, lxdui_current_version='2.0')

