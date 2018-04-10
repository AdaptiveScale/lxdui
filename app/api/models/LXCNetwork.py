from app.api.models.LXDModule import LXDModule
from pylxd import Client
import subprocess
from itertools import takewhile
from netaddr import IPAddress
import time
import socket
import struct


class LXCNetwork(LXDModule):

    def __init__(self, input):
        self.client = Client()
        self.input = input

        self.MAP = {"ipv4.address": ["IPv4_ENABLED", "IPv4_ADDR", "IPv4_NETMASK", "IPv4_AUTO"],
                    "ipv6.address": ["IPv6_ENABLED", "IPv6_ADDR", "IPv6_NETMASK", "IPv6_AUTO"],
                    "ipv4.nat": "IPv4_NAT",
                    "ipv6.nat": "IPv6_NAT",
                    "ipv4.dhcp": "IPv4_DHCP",
                    "ipv4.dhcp.ranges": ["IPv4_DHCP_START", "IPv4_DHCP_END"],
                    "ipv6.dhcp": "IPv6_DHCP",
                    "ipv6.dhcp.ranges": ["IPv6_DHCP_START", "IPv6_DHCP_END"]}
        self.AUTO_YAML_TERMS = ['auto', '"auto"', "'auto'"]
        self.NONE_YAML_TERMS = ['none', '"none"', "'none'"]
        self.TRUE_YAML_TERMS = ['true', '"true"', "'true'"]


    def info(self):
        try:
            tmp_start_reading = False
            used_by_containers = []
            p = subprocess.Popen(["lxc", "network", "show", self.input.get('name')], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            output_rez, err_rez = p.communicate()

            if err_rez.strip() == "error: not found":
                return {'error': True, "message": "LXD Network bridge {} does not exists !".format(name)}
            elif "is lxd installed and running" in str(err_rez).lower():
                return {'error': True,
                        "message": "We are having troubles connecting, this might be due to the LXD daemon not running !"}
            elif "command not found" in str(err_rez).lower():
                return {'error': True,
                        "message": "LXC seems to not be installed or the the LXD daemon might not running !"}
            else:
                # found
                p2 = subprocess.Popen(["lxc", "network", "show", self.input.get('name')], stdout=subprocess.PIPE)
                output_rez = p2.stdout.read()
                arr = str(output_rez).split("\\n")

                rez = list(takewhile(lambda line: line.strip() != "name: {}".format(self.input.get('name')), arr))

                # =====================================================================
                for k in arr:
                    k = k.strip()

                    if tmp_start_reading:
                        if len(k) > 18:
                            if (k[:18] == "- /1.0/containers/"):
                                used_by_containers.append(k[18:].strip())
                        else:
                            break;
                    if k[:7] == 'used_by':
                        tmp_start_reading = True

                return {'error': False, "result": self._structure_data(rez), 'used_by': used_by_containers}
        except Exception as e:
            raise ValueError(e)

    def createNetwork(self, input, name):
        try:
            return self._executeLXCNetworkTerminal(self._formToLXCSetTask(input), name)
        except Exception as e:
            raise ValueError(e)

    def deleteNetwork(self):
        try:
            p = subprocess.Popen(['lxc', 'network', 'delete', self.input.get('name')], stdout=subprocess.PIPE)
            return {'completed': True}
        except Exception as e:
            raise ValueError(e)

    def updateNetwork(self, input, name):
        try:
            return self._executeLXCNetworkTerminal(self._formToLXCSetTask(input), name)
        except Exception as e:
            raise ValueError(e)


    def _executeLXCNetworkTerminal(self, lines_to_exec, name):
        p = subprocess.Popen(["lxc", "network", "create", name], stdout=subprocess.PIPE)
        time.sleep(1)
        for lxc_network_value in lines_to_exec['unset']:
            p = subprocess.Popen(["lxc", "network", "unset", name, lxc_network_value],
                                 stdout=subprocess.PIPE)

            time.sleep(1)

        for l in lines_to_exec["set"]:
            LXC_NET_ATTR = list(l.keys())[0]
            LXC_NET_ATTR_VAL = l[LXC_NET_ATTR]
            p = subprocess.Popen(["lxc", "network", "set", name, LXC_NET_ATTR, LXC_NET_ATTR_VAL],
                                 stdout=subprocess.PIPE)

            time.sleep(1)

        return {"completed": True}


    def _formToLXCSetTask(self, data):
        TO_DOS = {"set": [], "unset": []}

        if data.get("IPv4_ENABLED") == False:
            TO_DOS["set"].append({"ipv4.address": "none"})
            TO_DOS["set"].append({"ipv4.nat": "false"})
        else:
            TO_DOS["set"].append({"ipv4.nat": "true"})
            if data.get("IPv4_AUTO") == True:
                TO_DOS["unset"].append("ipv4.dhcp.ranges")
                TO_DOS["set"].append({"ipv4.address": "auto"})
            else:
                CIDR_MASK = self._netmaskToCIDRSuffix(data.get("IPv4_NETMASK"))

                TO_DOS["set"].append({"ipv4.address": data.get("IPv4_ADDR") + '/' + CIDR_MASK})
                if data.get("IPv4_DHCP_START") and data.get("IPv4_DHCP_END"):
                    TO_DOS["set"].append(
                        {"ipv4.dhcp.ranges": data.get("IPv4_DHCP_START") + '-' + data.get("IPv4_DHCP_END")})

        return TO_DOS


    def _netmaskToCIDRSuffix(self, IP_MASK_ADDR):
        return str(IPAddress(IP_MASK_ADDR).netmask_bits())

    def _CIDR_suffix_to_netmask_ipv4(self, nr):
        host_bits = 32 - nr
        netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
        return netmask

    def _structure_data(self, linez):

        rez = {}

        for line in linez:
            sl = line.lstrip().lower()
            #print(sl)

            if sl[:12] == "ipv4.address":
                i = self.MAP["ipv4.address"]
                value = sl[sl.index(':') + 1:].strip()
                if value in self.NONE_YAML_TERMS:
                    rez[i[0]] = False
                elif value in self.AUTO_YAML_TERMS:
                    rez[i[0]] = True
                    rez[i[3]] = True
                else:
                    v = value.split('/')
                    rez[i[0]] = True
                    rez[i[3]] = False
                    rez[i[1]] = v[0]
                    rez[i[2]] = self._CIDR_suffix_to_netmask_ipv4(int(v[1]))

            elif sl[:16] == "ipv4.dhcp.ranges":
                i = self.MAP["ipv4.dhcp.ranges"]
                value = sl[sl.index(':') + 1:].strip().split('-')
                # start
                rez[i[0]] = value[0]
                rez[i[1]] = value[1]
            # finish

            # NAT <ipv4> and <ipv6>
            elif sl[:8] == "ipv4.nat":
                i = self.MAP["ipv4.nat"]
                value = sl[sl.index(':') + 1:].strip()
                rez[i] = True if (value in self.TRUE_YAML_TERMS) else False
            elif sl[:8] == "ipv6.nat":
                i = self.MAP["ipv6.nat"]
                value = sl[sl.index(':') + 1:].strip()
                rez[i] = True if (value in self.TRUE_YAML_TERMS) else False


            elif sl[:12] == "ipv6.address":
                i = self.MAP["ipv6.address"]
                # could be none
                value = sl[sl.index(':') + 1:].strip()
                if value in self.NONE_YAML_TERMS:
                    rez[i[0]] = False
                elif value in self.AUTO_YAML_TERMS:
                    rez[i[0]] = True
                    rez[i[3]] = True
                else:
                    v = value.split('/')
                    rez[i[0]] = True
                    rez[i[3]] = False
                    rez[i[1]] = v[0]
                    # without the translation
                    rez[i[2]] = int(v[1])

        return rez
