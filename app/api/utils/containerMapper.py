

def getContainerDetails(container):
    ip = 'N/A'
    if container.state().network != None:
        if  container.state().network.get('eth0') != None and len(container.state().network.get('eth0')['addresses']) > 0:
            ip = container.state().network['eth0']['addresses'][0].get('address', 'N/A')
        elif container.state().network.get('enp5s0') != None and len(container.state().network.get('enp5s0')['addresses']) > 0:
            ip = container.state().network['enp5s0']['addresses'][0].get('address', 'N/A')
        elif ip == 'N/A':
            found = False
            for network in container.state().network:
                for address in network:
                    if address['family'] == 'inet' and address['scope'] == 'global': 
                        ip = address['address']
                        found = True
                        break
                if found:
                    break

    image = 'N/A'
    if container.config.get('image.os') != None and container.config.get('image.release') != None and container.config.get('image.architecture') != None:
        image = ''.join(container.config.get('image.os') + ' ' + container.config.get('image.release') + ' ' + container.config.get('image.architecture'))

    instance_type = 'Container'
    if container.type == 'virtual-machine':
        instance_type = 'Virtual Machine'
    return {
        'name': container.name,
        'status': container.status,
        'ip': ip,
        'ephemeral': container.ephemeral,
        'type': instance_type,
        'image': image,
        'created_at': container.created_at
    }