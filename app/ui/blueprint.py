from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from app.api.models.LXCContainer import LXDModule

uiPages = Blueprint('uiPages', __name__, template_folder='./templates',
                    static_folder='./static')

@uiPages.route('/')
def index():
    return render_template('login.html', currentpage='Login')

@uiPages.route('/containers')
def container():
    containers = LXDModule().listContainers()
    return render_template('containers.html', currentpage='Containers',
                           containers=containers)

@uiPages.route('/profiles')
def profile():
    profiles = LXDModule().listProfiles()
    return render_template('profiles.html', currentpage='Profiles',
                           profiles=profiles)
@uiPages.route('/network')
def network():
    network = LXDModule().listNetworks()
    return render_template('network.html', currentpage='Network',
                           network=network)

@uiPages.route('/images')
def images():
    localImages = LXDModule().listLocalImages()
    remoteImages = LXDModule().listRemoteImages()
    return render_template('images.html', currentpage='Images',
                           localImages=localImages,
                           remoteImages=remoteImages)

