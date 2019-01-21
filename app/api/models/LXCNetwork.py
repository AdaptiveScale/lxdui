from app.api.models.LXDModule import LXDModule
from pylxd import Client
import subprocess
from itertools import takewhile
from netaddr import IPAddress
import time
import socket
import struct
import logging

logging = logging.getLogger(__name__)

class LXCNetwork(LXDModule):

    def __init__(self, input):
        logging.info('Connecting to LXD')
        super().__init__()
        logging.debug('Setting network input to {}'.format(input))
        self.input = input
        logging.debug('Setting network name to {}'.format(input.get('name')))
        self.name = input.get('name')

        super(LXCNetwork, self).__init__()
        try:
            self.network = self.client.networks.get(self.name)
        except:
            logging.debug('Network {} does not exist.'.format(self.name))
            self.network = None

    def info(self):
        try:
            logging.info('Reading network {} information'.format(self.name))

            config = {}

            if self.network.config.get('ipv4.address'):
                config['IPv4_ADDR'] = self.network.config.get('ipv4.address').split('/')[0]
                config['IPv4_NETMASK'] = self._CIDR_suffix_to_netmask_ipv4(
                    int(self.network.config.get('ipv4.address').split('/')[1]))
            
            config['IPv4_NAT'] = self.network.config.get('ipv4.nat')
            config['IPv4_DHCP'] = self.network.config.get('ipv4.dhcp')
            
            if self.network.config.get('ipv4.dhcp.ranges'):
                config['IPv4_DHCP_START'] = self.network.config.get('ipv4.dhcp.ranges').split('-')[0]
                config['IPv4_DHCP_END'] = self.network.config.get('ipv4.dhcp.ranges').split('-')[1]
            
            used_by = [ c[18:].strip() for c in self.network.used_by ]
            return {'error': False, "result": config, 'used_by': used_by}
        except Exception as e:
            logging.error('Failed to retrieve information for network {}'.format(self.name))
            logging.exception(e)
            raise ValueError(e)

    def createNetwork(self):
        try:
            logging.info('Creating network {}'.format(self.name))
            config = {
                'ipv4.address': '{}/{}'.format(self.input.get('IPv4_ADDR'),
                                               self._netmaskToCIDRSuffix(self.input.get('IPv4_NETMASK'))),
                'ipv4.nat': self.input.get('IPv4_NAT'),
                'ipv4.dhcp': self.input.get('IPv4_DHCP'),
                'ipv4.dhcp.ranges': '{}-{}'.format(self.input.get('IPv4_DHCP_START'),
                                                   self.input.get('IPv4_DHCP_END')),
            }
            self.client.networks.create(self.name, type='bridge', config=config)
            self.network = self.client.networks.get(self.name)
            return {"completed": True}
        except Exception as e:
            logging.error('Failed to create network {}'.format(self.name))
            logging.exception(e)
            raise ValueError(e)

    def deleteNetwork(self):
        try:
            logging.info('Deleting network {}'.format(self.name))
            self.network.delete()
            return {'completed': True}
        except Exception as e:
            logging.error('Failed to delete network {}'.format(self.name))
            logging.exception(e)
            raise ValueError(e)

    def updateNetwork(self):
        try:
            logging.info('Updating network {}'.format(self.name))

            logging.info(self.network.config)
            ipv4_cidr = self._netmaskToCIDRSuffix(self.input.get('IPv4_NETMASK'))
            self.network.config['ipv4.address'] = '{}/{}'.format(self.input.get('IPv4_ADDR'), ipv4_cidr)
            self.network.config['ipv4.nat'] = self.input.get('IPv4_NAT')
            self.network.config['ipv4.dhcp'] = self.input.get('IPv4_DHCP')
            self.network.config['ipv4.dhcp.ranges'] = '{}-{}'.format(self.input.get('IPv4_DHCP_START'),
                                                                     self.input.get('IPv4_DHCP_END'))
            self.network.save()
            return {"completed": True}
        except Exception as e:
            logging.error('Failed to update network {}'.format(self.name))
            logging.exception(e)
            raise ValueError(e)

    def _netmaskToCIDRSuffix(self, IP_MASK_ADDR):
        return str(IPAddress(IP_MASK_ADDR).netmask_bits())

    def _CIDR_suffix_to_netmask_ipv4(self, nr):
        host_bits = 32 - nr
        netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
        return netmask
