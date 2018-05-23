from flask import Blueprint, render_template
from app.api.models.LXCContainer import LXDModule, LXCContainer
from app.api.utils.containerMapper import getContainerDetails
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
            result.append(getContainerDetails(container))

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


@uiPages.route('/containers/<string:name>')
def containerDetails(name):
    try:
        container = LXCContainer({'name': name})
        return render_template('container-details.html', currentpage='Container Details',
                               container=container.info(),
                               profiles = getProfiles(),
                               lxdui_current_version=VERSION)
    except ValueError as ex:
        return render_template('container-details.html', currentpage='Container Details',
                               container=None,
                               name=name,
                               message=ex.__str__(),
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

@uiPages.route('/storage-pools')
def storagePools():
    try:
        storagePools = LXDModule().listStoragePools()
        return render_template('storage-pools.html', currentpage='StoragePools',
                               storagePools=storagePools, lxdui_current_version=VERSION)
    except:
        return render_template('storage-pools.html', currentpage='Profiles',
                               storagePools=[], lxdui_current_version=VERSION)

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
    localImages = getLocalImages()
    profiles = getProfiles()
    remoteImages = getRemoteImages()
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


def getLocalImages():
    try:
        localImages = LXDModule().listLocalImages()
    except:
        localImages = []

    return localImages

def getRemoteImages():
    try:
        remoteImages = LXDModule().listRemoteImages()
    except:
        remoteImages = []

    return remoteImages

def getProfiles():
    try:
        profiles = LXDModule().listProfiles()
    except:
        profiles = []

    return profiles

