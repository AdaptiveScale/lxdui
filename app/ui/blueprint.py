from flask import Blueprint, render_template
from app.api.models.LXCContainer import LXDModule, LXCContainer
from app.api.utils.containerMapper import getContainerDetails
from app.lib.conf import Config
from app import __metadata__ as meta
from app.__metadata__ import VERSION
from flask_jwt_extended import jwt_required
from jwt.exceptions import PyJWTError
from functools import wraps

import json
import os
import platform
import subprocess

uiPages = Blueprint('uiPages', __name__, template_folder='./templates',
                    static_folder='./static')

def jwt_ui(func):
    """
    Catches JWT Errors and returns an error page
    rather than a json encoded error.
    """
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        try:
            retval = func(*args, **kwargs)
        except PyJWTError as e:
            return render_template('auth_error.html', error=e)
        return retval
    return wrapper_function

def memory():
    mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    return int(mem_bytes / (1024. ** 2)) # convert to mb

@uiPages.route('/')
def index():
    return render_template('login.html', currentpage='Login')

@uiPages.route('/containers')
@jwt_ui
@jwt_required()
def container():
    try:
        containers = LXDModule().listContainers()
        result = []
        for container in containers:
            result.append(getContainerDetails(container))

        images = LXDModule().listLocalImages()
        profiles = LXDModule().listProfiles()
        storagePools = LXDModule().listStoragePools()
        limitsCPU = LXDModule().setLimitsCPU()
        # While Python does offer a cpu_count() function in their os library this function returns 
        # the number of CPU cores allocated to the UI container if LXDUI is installed in a container.
        # To get the number of cores of the host we have to execute 'lscpu' through the shell which 
        # returns all the data regarding the hosts physical CPU from which we can extract the maximum number of cores.
        cpuCount = subprocess.check_output("lscpu | grep 'CPU(s):' | head -1 | grep -o -E '[0-9]+' | tr -d '\n'", shell=True, text=True)

        return render_template('containers.html', currentpage='Containers',
                               containers=result,
                               images = images,
                               profiles = profiles,
                               memory = memory(),
                               limitsCPU = limitsCPU,
                               cpu = cpuCount,
                               storagePools = storagePools,
                               lxdui_current_version=VERSION)
    except:
        return render_template('containers.html', currentpage='Containers',
                               containers=[],
                               images=[],
                               profiles=[],
                               memory=memory(),
                               storagePools = [],
                               cpu = cpuCount,
                               limitsCPU = limitsCPU,
                               lxdui_current_version=VERSION)


@uiPages.route('/containers/<string:name>')
@jwt_ui
@jwt_required()
def containerDetails(name):
    try:
        container = LXCContainer({'name': name})
        return render_template('container-details.html', currentpage='Container Details',
                               container=container.info(),
                               profiles = getProfiles(),
                               networks = LXDModule().listNetworks(),
                               lxdui_current_version=VERSION)
    except ValueError as ex:
        return render_template('container-details.html', currentpage='Container Details',
                               container=None,
                               name=name,
                               message=ex.__str__(),
                               lxdui_current_version=VERSION)



@uiPages.route('/profiles')
@jwt_ui
@jwt_required()
def profile():
    try:
        profiles = LXDModule().listProfiles()
        return render_template('profiles.html', currentpage='Profiles',
                               profiles=profiles, lxdui_current_version=VERSION)
    except:
        return render_template('profiles.html', currentpage='Profiles',
                               profiles=[], lxdui_current_version=VERSION)

@uiPages.route('/storage-pools')
@jwt_ui
@jwt_required()
def storagePools():
    try:
        storagePools = LXDModule().listStoragePools()
        return render_template('storage-pools.html', currentpage='StoragePools',
                               storagePools=storagePools, lxdui_current_version=VERSION)
    except:
        return render_template('storage-pools.html', currentpage='Profiles',
                               storagePools=[], lxdui_current_version=VERSION)

@uiPages.route('/network')
@jwt_ui
@jwt_required()
def network():
    try:
        network = LXDModule().listNetworks()
        return render_template('network.html', currentpage='Network',
                               network=network, lxdui_current_version=VERSION)
    except:
        return render_template('network.html', currentpage='Network',
                               network=[], lxdui_current_version=VERSION)

@uiPages.route('/images')
@jwt_ui
@jwt_required()
def images():
    localImages = getLocalImages()
    profiles = getProfiles()
    remoteImages = []
    nightlyImages = []
    hubImages = getHubImages()
    remoteImagesLink = Config().get(meta.APP_NAME, '{}.images.remote'.format(meta.APP_NAME.lower()))
    return render_template('images.html', currentpage='Images',
                           localImages=localImages,
                           remoteImages=remoteImages,
                           nightlyImages=nightlyImages,
                           hubImages=hubImages,
                           profiles=profiles,
                           jsData={
                               'local': json.dumps(localImages),
                               'remote': json.dumps(remoteImages),
                               'nightly': json.dumps(nightlyImages),
                               'hub': json.dumps(hubImages)
                           },
                           memory=memory(),
                           lxdui_current_version=VERSION,
                           remoteImagesLink=remoteImagesLink,
                           imageHubLink=meta.IMAGE_HUB,
                           architecture=platform.machine())


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

def getNightlyImages():
    try:
        nightlyImages = LXDModule().listNightlyImages()
        images = []
        for image in nightlyImages:
            images.append(image['metadata'])
        nightlyImages=images
    except:
        nightlyImages = []

    return nightlyImages


def getHubImages():
    try:
        hubImages = LXDModule().listHubImages()
    except:
        hubImages = []

    return hubImages

def getProfiles():
    try:
        profiles = LXDModule().listProfiles()
    except:
        profiles = []

    return profiles

