import os
import subprocess
from itertools import takewhile
from netaddr import IPAddress
import socket
import struct
import re
import time

class BridgeNetwork():
	def __init__(self):
		self.MAP = { "ipv4.address" : ["IPv4_ENABLED", "IPv4_ADDR", "IPv4_NETMASK", "IPv4_AUTO"],
					 "ipv6.address" : ["IPv6_ENABLED", "IPv6_ADDR", "IPv6_NETMASK", "IPv6_AUTO"],
					 "ipv4.nat" : "IPv4_NAT",
					 "ipv6.nat" : "IPv6_NAT",
					 "ipv4.dhcp" : "IPv4_DHCP",
					 "ipv4.dhcp.ranges" : ["IPv4_DHCP_START", "IPv4_DHCP_END"],
					 "ipv6.dhcp" : "IPv6_DHCP",
					 "ipv6.dhcp.ranges" : ["IPv6_DHCP_START", "IPv6_DHCP_END"]}
		self.AUTO_YAML_TERMS = [ 'auto', '"auto"', "'auto'" ]
		self.NONE_YAML_TERMS = [ 'none', '"none"', "'none'" ]
		self.TRUE_YAML_TERMS = [ 'true' , '"true"' , "'true'"]

	def get_available_bridges(self):
		
		'''
		p = subprocess.Popen(["sudo", "lxc" , "network" , "list"], stdout = subprocess.PIPE, stderr=subprocess.PIPE)
		output_rez, err_rez = p.communicate()
		'''
		p = subprocess.Popen(["sudo", "lxc" , "network" , "show", "lxdbr0"], stdout = subprocess.PIPE, stderr=subprocess.PIPE)
		output_rez, err_rez = p.communicate()
		return str({ "ouput" : output_rez , 'err' : err_rez})

		arr = output_rez.split('\n')[3:-1]

		result = []
		for line in arr:
			if line[:1] != "+":
				terms = line.split('|')
				if terms[2].strip() == "bridge":
					result.append( { "name" : terms[1], "active" : True if terms[3].strip().lower() == "yes" else False })#, "term2" : terms[2] })

		return str(result)

	def get_lxd_main_bridge_config(self):
		tmp_start_reading = False
		used_by_containers = []
		p = subprocess.Popen(["sudo", "lxc" , "network" , "show", "lxdbr0"], stdout = subprocess.PIPE, stderr=subprocess.PIPE)
		output_rez, err_rez = p.communicate()

		if err_rez.strip() == "error: not found":
			return { 'error' : True,  "message" : "LXD Network bridge <b>lxdbr0</b> does not exists !" }
		elif "is lxd installed and running" in str(err_rez).lower():
			return { 'error' : True, "message" : "We are having troubles connecting, this might be due to the LXD daemon not running !" }
		elif "command not found" in str(err_rez).lower():
			return { 'error' : True, "message" : "LXC seems to not be installed or the the LXD daemon might not running !" }
		else:
			#found
			p2 = subprocess.Popen(["sudo", "lxc" , "network" , "show", "lxdbr0"], stdout = subprocess.PIPE)
			output_rez = p2.stdout.read()
			arr = output_rez.split('\n')[1:]

			rez = list(takewhile(lambda line: line.strip() != "name: lxdbr0", arr))
			#=====================================================================
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

			return { 'error' : False, "result" : self._structure_data(rez), 'used_by' : used_by_containers }
	
	def _structure_data(self, linez):
		
		rez = {}

		for line in linez:
			sl = line.lstrip().lower()
			#print sl
			
			if sl[:12] == "ipv4.address":
				i = self.MAP["ipv4.address"]
				value = sl[sl.index(':')+1:].strip()
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
				value = sl[sl.index(':')+1:].strip().split('-')
				#start
				rez[i[0]] = value[0]
				rez[i[1]] = value[1]
				#finish
			

			# NAT <ipv4> and <ipv6>
			elif sl[:8] == "ipv4.nat":
				i = self.MAP["ipv4.nat"]
				value = sl[sl.index(':')+1:].strip()
				rez[i] = True if (value in self.TRUE_YAML_TERMS) else False
			elif sl[:8] == "ipv6.nat":
				i = self.MAP["ipv6.nat"]
				value = sl[sl.index(':')+1:].strip()
				rez[i] = True if (value in self.TRUE_YAML_TERMS) else False
			
			
			elif sl[:12] == "ipv6.address":
				i = self.MAP["ipv6.address"]
				#could be none
				value = sl[sl.index(':')+1:].strip()
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
					#without the translation
					rez[i[2]] = int(v[1])
			
					
		return rez

	def _execute_LXC_NETWORK_TERMINAL(self, lines_to_exec):
		textline = ""
		for lxc_network_value in lines_to_exec['unset']:
			p = subprocess.Popen(["sudo", "lxc" , "network" , "unset", "lxdbr0", lxc_network_value], stdout = subprocess.PIPE)
			textline += "LXC UNSET <{0}> ,,,".format(lxc_network_value.upper())
			#print p.stdout.read()
			#----------------
			time.sleep(0.5)
			
		for l in lines_to_exec["set"]:
			LXC_NET_ATTR = l.keys()[0]
			LXC_NET_ATTR_VAL = l[LXC_NET_ATTR]
			p = subprocess.Popen(["sudo", "lxc" , "network" , "set", "lxdbr0", LXC_NET_ATTR, LXC_NET_ATTR_VAL], stdout = subprocess.PIPE)
			textline += "LXC SET <{0}> => <{1}> ,,,".format(LXC_NET_ATTR,LXC_NET_ATTR_VAL)
			#print p.stdout.read()
			#----------------
			time.sleep(0.5)

		return { "completed" : True, "spitout" : textline.replace('"', r'\"')}

		#p = subprocess.Popen(["sudo", "lxc" , "network" , "set", "lxdbr0", LXC_NET_ATTR, LXC_NET_ATTR_VAL], stdout = subprocess.PIPE)
		#output_rez = p.stdout.read()
		
	def _form_to_LXC_SET_TASK(self, data):
		TO_DOS = { "set" : [] , "unset" : [] }

		# >>> IPv (4) <<<
		if data.get("IPv4_ENABLED") == False:
			TO_DOS["set"].append({ "ipv4.address" : "none" })
			TO_DOS["set"].append({ "ipv4.nat" : "false"})
			#TO_DOS["unset"].append( "ipv4.dhcp.ranges") 
		else:
			TO_DOS["set"].append({ "ipv4.nat" : "true"})
			# >> IPv4 <auto> or <specified> <<
			if data.get("IPv4_AUTO") == True:
				TO_DOS["unset"].append( "ipv4.dhcp.ranges") 
				TO_DOS["set"].append({ "ipv4.address" : "auto" })
			else:
				CIDR_MASK = self._netmask_to_CIDR_suffix(data.get("IPv4_NETMASK"))

				TO_DOS["set"].append( { "ipv4.address" : data.get("IPv4_ADDR")+'/'+ CIDR_MASK })
				if data.has_key("IPv4_DHCP_START") and data.has_key("IPv4_DHCP_END"):
					TO_DOS["set"].append({ "ipv4.dhcp.ranges" : data.get("IPv4_DHCP_START")+'-'+data.get("IPv4_DHCP_END") })



		# >>> IPv (6) <<<
		if data.get("IPv6_ENABLED") == False:
			TO_DOS["set"].append({ "ipv6.address" : "none" })
			TO_DOS["set"].append({ "ipv6.nat" : "false"})
			#TO_DOS["unset"].append( "ipv6.dhcp.ranges")
		else:
			TO_DOS["set"].append({ "ipv6.nat" : "true"})
			# >> IPv6 <auto> or <specified> <<
			if data.get("IPv6_AUTO") == True:
				TO_DOS["unset"].append( "ipv6.dhcp.ranges") 
				TO_DOS["set"].append({ "ipv6.address" : "auto" })
			else:
				CIDR_MASK = data.get("IPv6_NETMASK")#self._netmask_to_CIDR_suffix(data.get("IPv6_NETMASK"))

				TO_DOS["set"].append( { "ipv6.address" : data.get("IPv6_ADDR") + CIDR_MASK } )
				if data.has_key("IPv6_DHCP_START") and data.has_key("IPv6_DHCP_END"):
					TO_DOS["set"].append( { "ipv6.dhcp.ranges" : data.get("IPv6_DHCP_START")+'-'+data.get("IPv6_DHCP_END") } )
		
		return TO_DOS
	
	#helper private functions
	def _netmask_to_CIDR_suffix(self, IP_MASK_ADDR):
		return str(IPAddress(IP_MASK_ADDR).netmask_bits())

	def _CIDR_suffix_to_netmask_ipv4(self, nr):
		host_bits = 32 - nr
		netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
		return netmask

	# IPv4 and IPv6 VALIDITY
	def _is_valid_ipv4(self, ip):
		pattern = re.compile(r"""
            ^
            (?:
            # Dotted variants:
            (?:
                # Decimal 1-255 (no leading 0's)
                [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
            |
                0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
            |
                0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
            )
            (?:                  # Repeat 0-3 times, separated by a dot
                \.
                (?:
                [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
                |
                0x0*[0-9a-f]{1,2}
                |
                0+[1-3]?[0-7]{0,2}
                )
            ){0,3}
            |
            0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
            |
            0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
            |
            # Decimal notation, 1-4294967295:
            429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
            42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
            4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
            )
            $
        """, re.VERBOSE | re.IGNORECASE)
		return pattern.match(ip) is not None
	
	def _is_valid_ipv6(self, ip):
		pattern = re.compile(r"""
            ^
            \s*                         # Leading whitespace
            (?!.*::.*::)                # Only a single whildcard allowed
            (?:(?!:)|:(?=:))            # Colon iff it would be part of a wildcard
            (?:                         # Repeat 6 times:
                [0-9a-f]{0,4}           #   A group of at most four hexadecimal digits
                (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
            ){6}                        #
            (?:                         # Either
                [0-9a-f]{0,4}           #   Another group
                (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
                [0-9a-f]{0,4}           #   Last group
                (?: (?<=::)             #   Colon iff preceeded by exacly one colon
                |  (?<!:)              #
                |  (?<=:) (?<!::) :    #
                )                      # OR
            |                          #   A v4 address with NO leading zeros 
                (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
                (?: \.
                    (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
                ){3}
            )
            \s*                         # Trailing whitespace
            $
        """, re.VERBOSE | re.IGNORECASE | re.DOTALL)
		return pattern.match(ip) is not None

	def _validate_ipv6_netmask(self, form_value):
		if form_value[0] != "/":
			return False
		
		nr = form_value[1:]
		if nr.isdigit():
			nr = int(nr)
			return (nr > 0 and nr <= 128)
		return False
		

	def validate_form(self, form):
		pass_this = {}
		#default
		pass_this["IPv4_ENABLED"] = True
		pass_this["IPv4_AUTO"] = False
		pass_this["IPv6_ENABLED"] = True
		pass_this["IPv6_AUTO"] = False
		
		# version 4
		if form.has_key("IPv4_ENABLED"):
			if form["IPv4_ENABLED"] == "false":
				pass_this["IPv4_ENABLED"] = False

		else:
			if form.has_key("IPv4_AUTO"):
				if form["IPv4_AUTO"] == "true":
					pass_this["IPv4_AUTO"] = True
			else:
				if form.has_key("IPv4_ADDR") and form.has_key("IPv4_NETMASK"):
					if self._is_valid_ipv4(form["IPv4_ADDR"]) and self._is_valid_ipv4(form["IPv4_NETMASK"]):
						pass_this["IPv4_ADDR"] = str(form["IPv4_ADDR"])
						pass_this["IPv4_NETMASK"] = str(form["IPv4_NETMASK"])
						#specific DHCP IPv4 ranges
						
						if form.has_key("IPv4_DHCP_START") and form.has_key("IPv4_DHCP_END"):
							if (form["IPv4_DHCP_START"].strip() == "") and (form["IPv4_DHCP_END"].strip() == ""):
								pass
							elif self._is_valid_ipv4(form["IPv4_DHCP_START"]) and self._is_valid_ipv4(form["IPv4_DHCP_END"]):
								pass_this["IPv4_DHCP_START"] = str(form["IPv4_DHCP_START"])
								pass_this["IPv4_DHCP_END"] = str(form["IPv4_DHCP_END"])
							else:
								return { "error" : True, "message" : "Both of the IPv4 DHCP ranges must respect the IPv4 IP format !" }

					else:
						return { "error" : True, "message" : "One of the <IPv4_ADDR> or <IPv4_NETMASK> doesn't fit the IPv4 format !!!"}
				else:
					return { "error" : True, "message" : "<IPv4_ADDR> and <IPv4_NETMASK> must be defined when <IPv4_AUTO> is off !"}
		# end version 4

		# start version 6
		if form.has_key("IPv6_ENABLED"):
			if form["IPv6_ENABLED"] == "false":
				pass_this["IPv6_ENABLED"] = False

		else:
			if form.has_key("IPv6_AUTO"):
				if form["IPv6_AUTO"] == "true":
					pass_this["IPv6_AUTO"] = True
			else:
				if form.has_key("IPv6_ADDR") and form.has_key("IPv6_NETMASK"):
					if ( self._is_valid_ipv6(form["IPv6_ADDR"].strip()) and self._validate_ipv6_netmask(form["IPv6_NETMASK"].strip()) ):
						pass_this["IPv6_ADDR"] = str(form["IPv6_ADDR"].strip())
						pass_this["IPv6_NETMASK"] = str(form["IPv6_NETMASK"].strip())
						#specific DHCP IPv4 ranges
						
						if form.has_key("IPv6_DHCP_START") and form.has_key("IPv6_DHCP_END"):
							if (form["IPv6_DHCP_START"].strip() == "") and (form["IPv6_DHCP_END"].strip() == ""):
								pass
							elif self._is_valid_ipv6(form["IPv6_DHCP_START"]) and self._is_valid_ipv6(form["IPv6_DHCP_END"]):
								pass_this["IPv6_DHCP_START"] = str(form["IPv6_DHCP_START"])
								pass_this["IPv6_DHCP_END"] = str(form["IPv6_DHCP_END"])
							else:
								return { "error" : True, "message" : "Both of the IPv6 DHCP ranges must respect the IPv6 IP format !" }

					else:
						return { "error" : True, "message" : "Either <IPv6_ADDR> doesn't fit the IPv6 format or <IPv6_NETMASK> doesn't fit the (slash)0-128 format !!!" }
				else:
					return { "error" : True, "message" : "<IPv6_ADDR> and <IPv6_NETMASK> must be defined when <IPv6_AUTO> is off !"}
		# end version 6

		return { "error" : False, "validated_data": pass_this }