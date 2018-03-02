from api.src.lib.log import Log
# import api.src.lib.log
from api.src.lib.conf import Config
import json
import configparser
import hashlib
import os
import logging
from pathlib import Path
from OpenSSL import crypto
from socket import gethostname

class Certificate(object):

    def __init__(self):
        self.auth_file = Config().get(APP_NAME, 'lxdui.auth.conf')
        self.cert_file = Config().get(APP_NAME, 'lxdui.ssl.cert')
        self.key, self.cert = self.create()

    # Create a self signed certificate
    @staticmethod
    def create():
        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 1024)

        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = "US"
        cert.get_subject().ST = "Texas"
        cert.get_subject().L = "Dallas"
        cert.get_subject().O = "AdaptiveScale, Inc."
        cert.get_subject().OU = "OU=AdaptiveScale, DN=com"
        cert.get_subject().CN = gethostname()
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha1')

        key = crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
        cert = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)

        return key, cert

    @staticmethod
    def save(file, data):
        try:
            with open(file, 'wb') as f:
                f.write(data)
        except (FileNotFoundError, IOError) as e:
            log.info('Unable to open file.')
            log.info(e)