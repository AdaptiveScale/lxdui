from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.api.models.LXDModule import LXDModule
from app.api.utils import response

lxd_api = Blueprint('lxd_api', __name__)

@lxd_api.route('/profile')
@jwt_required()
def profiles():
    try:
        client = LXDModule()
        return jsonify({'status': 200, 'message': 'ok', 'data': client.listProfiles()})
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@lxd_api.route('/network')
@jwt_required()
def networks():
    try:
        client = LXDModule()
        return jsonify({'status': 200, 'message': 'ok', 'data': client.listNetworks()})
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@lxd_api.route('/config')
@jwt_required()
def config():
    try:
        client = LXDModule()
        return response.replySuccess(client.config())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())
