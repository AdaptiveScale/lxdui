from flask import Blueprint, request
from flask_login import login_required

from api.src.models.LXDModule import LXDModule
from api.src.helpers.BridgeNetwork import BridgeNetwork
from api.src.helpers.networkSchema import doValidate
from api.src.utils import response

network_api = Blueprint('network_api', __name__)

@network_api.route('/')
@login_required
def network():
    try:
        client = LXDModule()
        return response.replySuccess(client.listNetworks())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())

@network_api.route('/<string:name>')
@login_required
def networkInfo(name):
    bridgeNet = BridgeNetwork()
    mainConfig = bridgeNet.get_lxd_main_bridge_config(name)
    if mainConfig['error']:
        return response.replyFailed(message=mainConfig['message'])

    return response.replySuccess(mainConfig['result'])

@network_api.route('/<string:name>', methods=['PUT'])
@login_required
def updateNetwork(name):
    input = request.get_json(silent=True)
    validation = doValidate(input)
    if validation:
        return response.replyFailed(message=validation.message)

    input['IPv6_ENABLED'] = False
    bridgeNet = BridgeNetwork()
    lxcTask = bridgeNet._form_to_LXC_SET_TASK(input)
    bridgeNet._execute_LXC_NETWORK_TERMINAL(lxcTask, name)

    # Restart Containers
    mainConfig = bridgeNet.get_lxd_main_bridge_config(name)
    return response.replySuccess(mainConfig['result'])

@network_api.route('/<string:name>', methods=['POST'])
@login_required
def creatNetwork(name):
    input = request.get_json(silent=True)
    validation = doValidate(input)
    if validation:
        return response.replyFailed(message=validation.message)

    input['IPv6_ENABLED'] = False
    bridgeNet = BridgeNetwork()
    lxcTask = bridgeNet._form_to_LXC_SET_TASK(input)
    bridgeNet._execute_LXC_NETWORK_TERMINAL(lxcTask, name)

    #Restart Containers
    mainConfig = bridgeNet.get_lxd_main_bridge_config(name)
    return response.replySuccess(mainConfig['result'])