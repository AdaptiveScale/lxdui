from flask import Blueprint, render_template, redirect
from app.api.models.LXCContainer import LXDModule, LXCContainer
import json

uiPages = Blueprint('uiPages', __name__, template_folder='./templates',
                    static_folder='./static')

@uiPages.route('/')
def index():
    return render_template('login.html', currentpage='Login')

@uiPages.route('/containers')
def container():
    containers = LXDModule().listContainers()
    result = []
    for container in containers:
        c = LXCContainer({'name': container.get('name')})
        result.append(c.info())
    images = LXDModule().listLocalImages()
    profiles = LXDModule().listProfiles()
    return render_template('containers.html', currentpage='Containers',
                           containers=result,
                           images = images,
                           profiles = profiles,
                           lxdui_current_version='2.0')

@uiPages.route('/profiles')
def profile():
    profiles = LXDModule().listProfiles()
    return render_template('profiles.html', currentpage='Profiles',
                           profiles=profiles, lxdui_current_version='2.0')
@uiPages.route('/network')
def network():
    network = LXDModule().listNetworks()
    return render_template('network.html', currentpage='Network',
                           network=network, lxdui_current_version='2.0')

@uiPages.route('/images')
def images():
    localImages = LXDModule().listLocalImages()
    profiles = LXDModule().listProfiles()
    try:
        remoteImages = LXDModule().listRemoteImages()
    except:
        remoteImages = []
        # TODO - log exception
    return render_template('images.html', currentpage='Images',
                           localImages=localImages,
                           remoteImages=remoteImages,
                           profiles=profiles,
                           jsData = {
                               'local': json.dumps(localImages),
                               'remote':json.dumps(remoteImages),
                           },
                           lxdui_current_version='2.0')