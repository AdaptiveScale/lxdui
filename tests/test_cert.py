from app.api.lib import cert, log as logger
import os
import pathlib
import unittest
import logging

log = logging.getLogger(__name__)


class TestConfig(unittest.TestCase):

    @classmethod
    def setUp(cls):
        logger.Log('test')
        pass

    @classmethod
    def tearDown(cls):
        pass

    def test_logger(self):
        l = logger.Log('test')
        self.assertIsInstance(l, logger.Log)

    def test_cert(self):
        c = cert.Certificate()
        print('key file = {}'.format(c.key_file))
        print('cert file = {}'.format(c.cert_file))
        print('key = {}'.format(c.key))
        print('cert = {}'.format(c.cert))
        self.assertEqual(c.key_file, 'client.key')
        self.assertEqual(c.cert_file, 'client.crt')
        self.assertRegex(bytes.decode(c.key), r'^-----BEGIN PRIVATE KEY-----.*')
        self.assertRegex(bytes.decode(c.cert), r'^-----BEGIN CERTIFICATE-----.*')

    def test_save(self):

        def delete(file):
            if pathlib.Path(file).exists():
                os.remove(file)

        c = cert.Certificate()
        key = os.path.abspath(os.path.join('../conf', c.key_file))
        crt = os.path.abspath(os.path.join('../conf', c.cert_file))
        delete(key)
        delete(crt)
        c.save(key, c.key)
        c.save(crt, c.cert)
        self.assertEqual(os.stat(key).st_size, c.key.__len__() )
        self.assertEqual(os.stat(crt).st_size, c.cert.__len__())



if __name__ == '__main__':
    unittest.main()