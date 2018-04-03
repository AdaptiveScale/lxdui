from flask import Blueprint, render_template, redirect
from app.api.models.LXCContainer import LXDModule, LXCContainer
from app.__metadata__ import VERSION
import json
import os

uiPages = Blueprint('uiPages', __name__, template_folder='./templates',
                    static_folder='./static')

def memory():
    mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    return int(mem_bytes / (1024. ** 2)) # convert to mb

@uiPages.route('/')
def index():
    return render_template('login.html', currentpage='Login')

@uiPages.route('/containers')
def container():
    try:
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
                               memory=memory(),
                               lxdui_current_version=VERSION)
    except:
        return render_template('containers.html', currentpage='Containers',
                               containers=[],
                               images=[],
                               profiles=[],
                               memory=memory(),
                               lxdui_current_version=VERSION)

@uiPages.route('/profiles')
def profile():
    try:
        profiles = LXDModule().listProfiles()
        return render_template('profiles.html', currentpage='Profiles',
                               profiles=profiles, lxdui_current_version=VERSION)
    except:
        return render_template('profiles.html', currentpage='Profiles',
                               profiles=[], lxdui_current_version=VERSION)

@uiPages.route('/network')
def network():
    try:
        network = LXDModule().listNetworks()
        return render_template('network.html', currentpage='Network',
                               network=network, lxdui_current_version=VERSION)
    except:
        return render_template('network.html', currentpage='Network',
                               network=[], lxdui_current_version=VERSION)

@uiPages.route('/images')
def images():
    try:
        localImages = LXDModule().listLocalImages()
        profiles = LXDModule().listProfiles()
        remoteImages = LXDModule().listRemoteImages()
        return render_template('images.html', currentpage='Images',
                               localImages=localImages,
                               remoteImages=remoteImages,
                               profiles=profiles,
                               jsData={
                                   'local': json.dumps(localImages),
                                   'remote': json.dumps(remoteImages),
                               },
                               memory=memory(),
                               lxdui_current_version=VERSION)
    except:
        # TODO - log exception
        return render_template('images.html', currentpage='Images',
                               localImages=[],
                               remoteImages=[],
                               profiles=[],
                               jsData={
                                   'local': json.dumps([]),
                                   'remote': json.dumps([]),
                               },
                               memory=memory(),
                               lxdui_current_version=VERSION)
