from flask import Blueprint, abort, jsonify
from flask_login import login_required

from api.src.models.LXDModule import LXDModule
from api.src.utils import response

lxd_api = Blueprint('lxd_api', __name__)

@lxd_api.route('/profile')
@login_required
def profiles():
    try:
        client = LXDModule()
        return jsonify({'status': 200, 'message': 'ok', 'data': client.listProfiles()})
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@lxd_api.route('/network')
@login_required
def networks():
    try:
        client = LXDModule()
        return jsonify({'status': 200, 'message': 'ok', 'data': client.listNetworks()})
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@lxd_api.route('/config')
@login_required
def config():
    try:
        client = LXDModule()
        return response.replySuccess(client.config())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())