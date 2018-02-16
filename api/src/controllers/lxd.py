from flask import Blueprint, abort, jsonify

from api.src.models.LXDModule import LXDModule
from api.src.models.LXCContainer import LXCContainer

lxd_api = Blueprint('lxd_api', __name__)

@lxd_api.route('/container')
def containers():
    client = LXDModule()
    return jsonify({'status': 200, 'message': 'ok', 'data': client.listContainers()})


@lxd_api.route('/image')
def images():
    client = LXDModule()
    return jsonify({'status': 200, 'message': 'ok', 'data': client.listLocalImages()})


@lxd_api.route('/profile')
def profiles():
    client = LXDModule()
    return jsonify({'status': 200, 'message': 'ok', 'data': client.listProfiles()})


@lxd_api.route('/network')
def networks():
    client = LXDModule()
    return jsonify({'status': 200, 'message': 'ok', 'data': client.listNetworks()})


@lxd_api.route('/config')
def config():
    client = LXDModule()
    return jsonify({'status': 200, 'message': 'ok', 'data': client.config()})


@lxd_api.route('/container/<string:alias>')
def infoContainer(alias):
    container = LXCContainer({'alias': alias})
    return jsonify({'status': 200, 'message': 'ok', 'data': container.info()})


@lxd_api.route('/container/delete/<string:alias>', methods=['DELETE'])
def deleteContainer(alias):
    container = LXCContainer({'alias': alias})
    container.delete()
    return jsonify({'status': 200, 'message': 'ok', 'data': []})


@lxd_api.route('/container/start/<string:alias>', methods=['PUT'])
def startContainer(alias):
    container = LXCContainer({'alias': alias})
    container.start()
    return jsonify({'status': 200, 'message': 'ok', 'data': []})


@lxd_api.route('/container/stop/<string:alias>', methods=['PUT'])
def stopContainer(alias):
    container = LXCContainer({'alias': alias})
    container.stop()
    return jsonify({'status': 200, 'message': 'ok', 'data': []})


@lxd_api.route('/container/restart/<string:alias>', methods=['PUT'])
def restartContainer(alias):
    container = LXCContainer({'alias': alias})
    container.restart()
    return jsonify({'status': 200, 'message': 'ok', 'data': []})


@lxd_api.route('/container/snapshot/<string:alias>')
def containerSnapshots(alias):
    container = LXCContainer({'alias': alias})
    return jsonify({'status': 200, 'message': 'ok', 'data': container.snapshot()})