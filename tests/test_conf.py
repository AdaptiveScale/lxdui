from app import __metadata__ as meta
import app.lib.conf as conf
import app.lib.log as logger
import os
import pathlib
import time
import configparser
import unittest
import logging

log = logging.getLogger(__name__)


class TestConfig(unittest.TestCase):

    @classmethod
    def setUp(cls):
        conf_file = '../conf/lxdui.conf'
        empty_file = '../conf/lxdui.conf.empty'

        # create the sample conf file
        file = pathlib.Path(conf_file)
        if not file.exists() or (file.exists() and file.stat() == 0 ):
            with open(conf_file, 'w') as f:
                f.write(meta.__default_config__)

        # create the empty conf file
        if not pathlib.Path(empty_file).exists():
            with open(empty_file, 'a'):
                os.utime(empty_file, None)

    @classmethod
    def tearDown(cls):
        empty_file = '../conf/lxdui.conf.empty'
        # remove the empty conf file
        if pathlib.Path(empty_file).exists():
            os.remove(empty_file)

    def test_logger(self):
        l = logger.Log('test')
        self.assertIsInstance(l, logger.Log)

    def test_external_config_fnf(self):
        # assert = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            conf.Config(conf='../conf/lxdui.conf.bad')

    def test_external_config_empty_file(self):
        # assert = FileNotFoundError
        file = '../conf/lxdui.conf'
        if pathlib.Path(file).exists():
            os.remove(file)
        with self.assertRaises(Exception):
            conf.Config(conf='../conf/lxdui.conf.empty')

    def test_external_config(self):
        # assert = Config object
        c = conf.Config(conf='../conf/lxdui.conf')
        self.assertIsInstance(c, conf.Config)


    def test_ini_config(self):
        # assert = Config object
        c = conf.Config()
        self.assertIsInstance(c, conf.Config)

    def test_meta_config(self):
        # Tests the case when no conf file exists
        # assert = Config object (using default config from meta)
        file = '../conf/lxdui.conf'
        if pathlib.Path(file).exists():
            os.remove(file)
        time.sleep(1)
        c = conf.Config()
        self.assertIsInstance(c, conf.Config)

    def test_envGet(self):
        c = conf.Config()
        log_path = c.log_file
        conf_path = c.config_file
        d1 = c.envGet()
        d2 = {'LXDUI_CONF': conf_path, 'LXDUI_LOG': log_path}
        self.assertDictEqual(d1, d2)

    def test_envSet(self):
        c = conf.Config()
        log_path = '/path/to/log/file'
        conf_path = '/path/to/conf/file'
        c.envSet(log=log_path, conf=conf_path)
        d1 = c.envGet()
        d2 = {'LXDUI_CONF': conf_path, 'LXDUI_LOG': log_path}
        self.assertDictEqual(d1, d2)

    def test_envShow(self):
        conf.Config().envShow()

    def test_config_show(self):
        print('='*120)
        conf.Config().show()
        print('=' * 120)

    # def test_getAbsPath(self):
    #     dir = 'conf'
    #     file = 'lxdui.conf'
    #     absPath = conf.Config().getAbsPath(dir, file)
    #     expected_path = os.path.join(os.path.abspath(dir), file)
    #     self.assertEqual(absPath, expected_path)

    def test_getConfig(self):
        file = pathlib.Path('../conf/lxdui.conf')
        c = conf.Config().getConfig(file)
        self.assertIsInstance(c, configparser.ConfigParser)

    def test_getConfig_fnf(self):
        # assert = FileNotFoundError
        file = pathlib.Path('../conf/lxdui.conf.bad')
        with self.assertRaises(FileNotFoundError):
            conf.Config().getConfig(file)

    def test_parseConfig(self):
        # assert = configparser.ConfigParser
        file = pathlib.Path('../conf/lxdui.conf')
        c = conf.Config().parseConfig(file)
        self.assertIsInstance(c, configparser.ConfigParser)

    def test_parseConfig_empty(self):
        # assert = Exception
        file = pathlib.Path('../conf/lxdui.conf.empty')
        with self.assertRaises(Exception):
            conf.Config.parseConfig(file)

    # def test_findConf_(self):
    #     dir = 'conf'
    #     file = 'lxdui.conf'
    #     absPath = conf.Config().getAbsPath(dir, file)
    #     expected_path = os.path.join(os.path.abspath(dir), file)
    #     self.assertEqual(absPath, expected_path)

    # def test_findConf_fnf(self):
    #     # assert = FileNotFoundError
    #     dir = pathlib.Path('conf')
    #     file = 'lxdui.conf.bad'
    #     with self.assertRaises(FileNotFoundError):
    #         conf.Config().findConf(dir, file)

    def test_save(self):
        file = pathlib.Path('../conf/lxdui.conf')
        file_before = 0
        file_after = 0

        if file.exists():
            file_before = file.stat()

        conf.Config().save()
        file_after = file.stat()
        self.assertEqual(file_before, file_after)

    def test_get(self):
        c = conf.Config().get('LXDUI', 'lxdui.port')
        self.assertEqual(c, '15151')

    def test_set(self):
        c = conf.Config()
        c.set('LXDUI', 'lxdui.port', '9999')
        port = c.config.get('LXDUI', 'lxdui.port')
        self.assertEqual(port, '9999')

    # def test_load_meta(self):
    #     c = conf.Config().load('meta')
    #     self.assertIsInstance(c, configparser.ConfigParser)

    def test_load_not_unknown(self):
        with self.assertRaises(Exception):
            conf.Config().load('foo')

if __name__ == '__main__':
    unittest.main()