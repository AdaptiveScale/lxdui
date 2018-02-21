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
        return response.replyFailed(message=e.__str__())


@lxd_api.route('/profile')
def profiles():
    try:
        client = LXDModule()
        return jsonify({'status': 200, 'message': 'ok', 'data': client.listProfiles()})
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@lxd_api.route('/network')
def networks():
    try:
        client = LXDModule()
        return jsonify({'status': 200, 'message': 'ok', 'data': client.listNetworks()})
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@lxd_api.route('/config')
def config():
    try:
        client = LXDModule()
        return response.replySuccess(client.config())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())