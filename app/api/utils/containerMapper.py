import re

def getContainerDetails(container):
    ip = []

    # Retrieve all IPv4 addresses with global scope
    instanceNetwork = container.state().network
    if instanceNetwork != None:
        for network_interface in instanceNetwork:
            current_network = instanceNetwork.get(network_interface)
            network_addresses = current_network.get('addresses')
            if len(network_addresses) > 0:
                for address in network_addresses:
                    if isIPV4(address.get('address')) and (address.get('scope') == 'global'):
                        ip.append(address.get('address'))

    # in case no IP addresses were found in all the previous network interfaces
    if len(ip) == 0:
        ip = 'N/A'

    image = 'N/A'
    if container.config.get('image.os') != None and container.config.get('image.release') != None and container.config.get('image.architecture') != None:
        image = ''.join(container.config.get('image.os') + ' ' + container.config.get('image.release') + ' ' + container.config.get('image.architecture'))

    instance_type = 'Container'
    if container.type == 'virtual-machine':
        instance_type = 'Virtual Machine'

    memory = container.config.get('limits.memory')
    if memory is None:
        memory = 'N/A'

    cpu = container.config.get('limits.cpu')
    if cpu is None:
        cpu = 'N/A'

    try:
        # attempt to extract the size of the root disk
        disk = container.devices.get('root')['size']
    except:
        # in case the root device was not set (passed on through profile)
        disk = 'N/A'

    return {
        'name': container.name,
        'status': container.status,
        'ip': ip,
        'memory': memory,
        'cpu': cpu,
        'disk': disk,
        'ephemeral': container.ephemeral,
        'type': instance_type,
        'image': image,
        'created_at': container.created_at,
    }

def isIPV4(address):

    valid = re.match('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', address)

    if valid:
        return True
    else:
        return False
