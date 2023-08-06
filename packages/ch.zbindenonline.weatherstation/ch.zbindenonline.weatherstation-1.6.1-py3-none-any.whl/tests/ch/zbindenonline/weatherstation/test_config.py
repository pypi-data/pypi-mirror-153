import os
import sys
import tempfile
import unittest
from unittest.mock import patch

from ch.zbindenonline.weatherstation.config import read_configuration


class ConfigTest(unittest.TestCase):
    def test_create_config_file_not_found(self):
        with patch.object(sys, 'argv', ['', '-c', 'missing_file.cfg']):
            with self.assertRaises(FileNotFoundError):
                read_configuration()

    def test_create_config(self):
        test_dir = tempfile.mkdtemp()
        cfg_path = os.path.join(test_dir, 'test.cfg')
        with open(cfg_path, 'w') as cfg_file:
            cfg_file.writelines(['[DEFAULT]\n',
                                 'sensors = {\n',
                                 '          "4711" : {"name":"mein test sensor"}\n',
                                 '          }\n',
                                 '[rest]\n',
                                 'url = https://example.com/api\n',
                                 'username = myholyuser\n',
                                 'password = theevenmoreholypassword\n',
                                 '[pictures]\n',
                                 'picture_dir = /path/to/pictures\n',
                                 'picture_url = https://testdomain.org/pictures\n',
                                 'username = picturesUser\n',
                                 'password = picturesPassword\n',
                                 'client_id = 17\n',
                                 'client_secret = a_long_secret\n',
                                 'delete_after_publish = false\n'
                                 ])
        with patch.object(sys, 'argv', ['', '-c', cfg_path]):
            config = read_configuration()
            self.assertEqual('https://example.com/api', config.rest.url)
            self.assertEqual('myholyuser', config.rest.username)
            self.assertEqual('theevenmoreholypassword', config.rest.password)

            self.assertEqual('/path/to/pictures', config.pictures.picture_dir)
            self.assertEqual('https://testdomain.org/pictures', config.pictures.picture_url)
            self.assertEqual('picturesUser', config.pictures.username)
            self.assertEqual('picturesPassword', config.pictures.password)
            self.assertEqual('17', config.pictures.client_id)
            self.assertEqual('a_long_secret', config.pictures.client_secret)
            self.assertFalse(config.pictures.delete_after_publish)
