from flask import Blueprint, request
from flask_jwt import jwt_required

from app.api.models.LXDModule import LXDModule
from app.api.models.LXCContainer import LXCContainer
from app.api.models.LXCNetwork import LXCNetwork
from app.api.schemas.networkSchema import doValidate
from app.api.utils import response

network_api = Blueprint('network_api', __name__)

@network_api.route('/')
@jwt_required()
def network():
    try:
        client = LXDModule()
        return response.replySuccess(client.listNetworks())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())

@network_api.route('/<string:name>')
@jwt_required()
def networkInfo(name):
    network = LXCNetwork({'name': name})
    mainConfig = network.info()
    if mainConfig['error']:
        return response.replyFailed(message=mainConfig['message'])

    return response.replySuccess(mainConfig['result'])

@network_api.route('/<string:name>', methods=['PUT'])
@jwt_required()
def updateNetwork(name):
    input = request.get_json(silent=True)
    validation = doValidate(input)
    if validation:
        return response.replyFailed(message=validation.message)

    input['IPv6_ENABLED'] = False

    network = LXCNetwork({'name': name})
    network.updateNetwork(input, name)

    mainConfig = network.info()
    for container in mainConfig['used_by']:
        LXCContainer({'name': container}).restart()
    return response.replySuccess(mainConfig['result'])

@network_api.route('/<string:name>', methods=['POST'])
@jwt_required()
def creatNetwork(name):
    input = request.get_json(silent=True)
    validation = doValidate(input)
    if validation:
        return response.replyFailed(message=validation.message)

    input['IPv6_ENABLED'] = False
    network = LXCNetwork({'name': name})
    network.createNetwork(input, name)

    mainConfig = network.info()
    return response.replySuccess(mainConfig['result'])

@network_api.route('/<string:name>', methods=['DELETE'])
@jwt_required()
def deleteNetwork(name):
    network = LXCNetwork({'name': name})
    network.deleteNetwork()

    client = LXDModule()
    return response.replySuccess(client.listNetworks())