from flask import Blueprint, request

from api.src.helpers.BridgeNetwork import BridgeNetwork
from api.src.utils import response

network_api = Blueprint('network_api', __name__)

@network_api.route('/')
def network():
    bridgeNet = BridgeNetwork()
    mainConfig = bridgeNet.get_lxd_main_bridge_config()
    if mainConfig['error']:
        return response.replyFailed(message=mainConfig['message'])

    return response.replySuccess(mainConfig['result'])

@network_api.route('/', methods=['POST'])
def creatNetwork():
    inputData = {
        'IPv4_ENABLED': True,
        'IPv4_AUTO': False,
        'IPv4_ADDR': '10.10.5.1',
        'IPv4_NETMASK': '255.255.255.0',
        'IPv4_DHCP_START': '10.10.5.100',
        'IPv4_DHCP_END': '10.10.5.200',
        'IPv6_ENABLED': False
    }

    bridgeNet = BridgeNetwork()
    lxcTask = bridgeNet._form_to_LXC_SET_TASK(inputData)
    executed = bridgeNet._execute_LXC_NETWORK_TERMINAL(lxcTask)

    #Restart Containers
    mainConfig = bridgeNet.get_lxd_main_bridge_config()
    return response.replySuccess(mainConfig['result'])