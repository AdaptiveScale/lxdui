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


@lxd_api.route('/container/<string:name>')
def infoContainer(name):
    container = LXCContainer({'name': name})
    return jsonify({'status': 200, 'message': 'ok', 'data': container.info()})


@lxd_api.route('/container/delete/<string:name>', methods=['DELETE'])
def deleteContainer(name):
    container = LXCContainer({'name': name})
    container.delete()
    return jsonify({'status': 200, 'message': 'ok', 'data': []})


@lxd_api.route('/container/start/<string:name>', methods=['PUT'])
def startContainer(name):
    container = LXCContainer({'name': name})
    container.start()
    return jsonify({'status': 200, 'message': 'ok', 'data': []})


@lxd_api.route('/container/stop/<string:name>', methods=['PUT'])
def stopContainer(name):
    container = LXCContainer({'name': name})
    container.stop()
    return jsonify({'status': 200, 'message': 'ok', 'data': []})


@lxd_api.route('/container/restart/<string:name>', methods=['PUT'])
def restartContainer(name):
    container = LXCContainer({'name': name})
    container.restart()
    return jsonify({'status': 200, 'message': 'ok', 'data': []})


@lxd_api.route('/container/snapshot/<string:name>')
def containerSnapshots(name):
    container = LXCContainer({'name': name})
    return jsonify({'status': 200, 'message': 'ok', 'data': container.snapshot()})