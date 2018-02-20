from flask import Blueprint, abort, jsonify

from api.src.models.LXDModule import LXDModule
from api.src.models.LXCContainer import LXCContainer
from api.src.utils import response

lxd_api = Blueprint('lxd_api', __name__)


@lxd_api.route('/image')
def images():
    try:
        client = LXDModule()
        return jsonify({'status': 200, 'message': 'ok', 'data': client.listLocalImages()})
    except ValueError as e:
        return response.reply(e.__str__(), 'Failed', 400)


@lxd_api.route('/profile')
def profiles():
    try:
        client = LXDModule()
        return jsonify({'status': 200, 'message': 'ok', 'data': client.listProfiles()})
    except ValueError as e:
        return response.reply(e.__str__(), 'Failed', 400)


@lxd_api.route('/network')
def networks():
    try:
        client = LXDModule()
        return jsonify({'status': 200, 'message': 'ok', 'data': client.listNetworks()})
    except ValueError as e:
        return response.reply(e.__str__(), 'Failed', 400)


@lxd_api.route('/config')
def config():
    try:
        client = LXDModule()
        return jsonify({'status': 200, 'message': 'ok', 'data': client.config()})
    except ValueError as e:
        return response.reply(e.__str__(), 'Failed', 400)

@lxd_api.route('/container/<string:name>')
def infoContainer(name):
    try:
        container = LXCContainer({'name': name})
        return jsonify({'status': 200, 'message': 'ok', 'data': container.info()})
    except ValueError as e:
        return response.reply(e.__str__(), 'Failed', 400)


@lxd_api.route('/container/start/<string:name>', methods=['PUT'])
def startContainer(name):
    try:
        container = LXCContainer({'name': name})
        container.start()
        return jsonify({'status': 200, 'message': 'ok', 'data': []})
    except ValueError as e:
        return response.reply(e.__str__(), 'Failed', 400)


@lxd_api.route('/container/stop/<string:name>', methods=['PUT'])
def stopContainer(name):
    try:
        container = LXCContainer({'name': name})
        container.stop()
        return jsonify({'status': 200, 'message': 'ok', 'data': []})
    except ValueError as e:
        return response.reply(e.__str__(), 'Failed', 400)


@lxd_api.route('/container/restart/<string:name>', methods=['PUT'])
def restartContainer(name):
    try:
        container = LXCContainer({'name': name})
        container.restart()
        return jsonify({'status': 200, 'message': 'ok', 'data': []})
    except ValueError as e:
        return response.reply(e.__str__(), 'Failed', 400)


@lxd_api.route('/container/snapshot/<string:name>')
def containerSnapshots(name):
    try:
        container = LXCContainer({'name': name})
        return jsonify({'status': 200, 'message': 'ok', 'data': container.snapshot()})
    except ValueError as e:
        return response.reply(e.__str__(), 'Failed', 400)