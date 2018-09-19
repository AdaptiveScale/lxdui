APP_NAME = 'LXDUI'
APP_CLI_CMD = 'lxdui'
VERSION = '2.2'
GIT_URL = 'https://github.com/AdaptiveScale/lxdui.git'
LXD_URL = 'http://localhost:8443'
LICENSE = 'Apache 2.0'
AUTHOR = 'AdaptiveScale, Inc.'
AUTHOR_URL = 'http://www.adaptivescale.com'
AUTHOR_EMAIL = 'info@adaptivescale.com'
KEYWORDS = 'lxc lxc-containers lxd'
IMAGE_HUB = 'http://hub.kuti.io'

'''

The following section is for the default configuration  
that will be written to the lxdui.conf file if the file 
does not already exist.

'''
AUTO_LOAD_CONFIG = True
DEFAULT_CONFIG_FORMAT = 'ini'
__default_config__ = """
[LXDUI]
lxdui.port = 15151
lxdui.images.remote = https://images.linuxcontainers.org
#lxdui.lxd.remote = https://lxd.host.org:8443/
#lxdui.lxd.sslverify = true
lxdui.jwt.token.expiration = 1200
lxdui.jwt.secret.key = AC8d83&21Almnis710sds
lxdui.jwt.auth.url.rule = /api/user/login
lxdui.admin.user = admin
lxdui.conf.dir = {{app_root}}/conf
lxdui.conf.file = ${lxdui.conf.dir}/lxdui.conf
lxdui.auth.conf = ${lxdui.conf.dir}/auth.conf
lxdui.ssl.cert = ${lxdui.conf.dir}/client.crt
lxdui.ssl.key = ${lxdui.conf.dir}/client.key
lxdui.log.dir =  {{app_root}}/logs
lxdui.log.file = ${lxdui.log.dir}/lxdui.log
lxdui.log.conf = ${lxdui.conf.dir}/log.conf
#lxdui.log.rotate = true
#lxdui.log.max = 10M
#lxdui.log.keep.generations = 5
lxdui.profiles = ${lxdui.conf.dir}/profiles
lxdui.zfs.pool.name = lxdpool
lxdui.app.alias = LXDUI
lxdui.cli = cli
        
[LXDUI_CERT]
lxdui.cert.country = US
lxdui.cert.state = Texas
lxdui.cert.locale = Dallas
lxdui.cert.org = AdaptiveScale, Inc.
lxdui.cert.ou = OU=AdaptiveScale, DN=com

[LXD]
lxd.bridge.enabled = true
lxd.bridge.name = lxdbr0
lxd.dns.conf.file = 
lxd.dns.domain = lxd
lxd.ipv4.addr = 10.5.5.1
lxd.ipv4.netmask = 255.255.255.0
lxd.ipv4.network = 10.5.5.0/24
lxd.ipv4.dhcp.range = 253
lxd.ipv4.dhcp.max = 10.5.5.2,10.5.5.254
lxd.ipv4.nat = true
lxd.ipv6.addr = 2001:470:b368:4242::1
lxd.ipv6.mask = 255.255.255.0
lxd.ipv6.network = 2001:470:b368:4242::/64
lxd.ipv6.nat = false
lxd.ipv6.proxy = false
"""

