from app.lib import conf
from OpenSSL import crypto
from socket import gethostname
from app import __metadata__ as meta
import logging

log = logging.getLogger(__name__)

class Certificate(object):

    def __init__(self):
        self.conf = conf.Config()
        self.key_file = self.conf.get(meta.APP_NAME, 'lxdui.ssl.key')
        self.cert_file = self.conf.get(meta.APP_NAME, 'lxdui.ssl.cert')
        self.key, self.cert = self.create()

    # Create a self signed certificate
    def create(self):
        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 1024)

        # set the certificate configuration parameters
        section = meta.APP_NAME + '_CERT'
        country = self.conf.get(section, 'lxdui.cert.country')
        state = self.conf.get(section, 'lxdui.cert.state')
        locale = self.conf.get(section, 'lxdui.cert.locale')
        org = self.conf.get(section, 'lxdui.cert.org')
        ou = self.conf.get(section, 'lxdui.cert.ou')

        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = country
        cert.get_subject().ST = state
        cert.get_subject().L = locale
        cert.get_subject().O = org
        cert.get_subject().OU = ou
        cert.get_subject().CN = gethostname()
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha256')

        #create the key and the cert
        key = crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
        cert = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
        # log.debug(key)
        # log.debug(cert)
        return key, cert

    @staticmethod
    def save(file, data):
        try:
            with open(file, 'wb') as f:
                f.write(data)
        except (FileNotFoundError, IOError) as e:
            log.info('Unable to open file.')
            log.info(e)