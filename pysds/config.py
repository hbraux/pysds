# -*- coding: utf-8 -*-

"""Application Configuration"""
import configparser
import logging
import os

from pysds.singleton import Singleton

CONFIG_PATH = os.path.expanduser(os.getenv('SDS_CONFIG_PATH', '~/.sds'))
CONFIG_FILE = "/sds.ini"
# TEMPORARY as longer keys take time for generation
KEY_LENGTH = 512

logger = logging.getLogger(__name__)


class Config(metaclass=Singleton):
    """This singleton handles application configuration"""

    def __init__(self, config_path=CONFIG_PATH, key_length=KEY_LENGTH, db_url=None):
        self.config_path = config_path
        self.key_length = key_length
        self.db_url = db_url or self._read('DatabaseUrl')

    @staticmethod
    def create(config_path=CONFIG_PATH):
        if not os.path.isdir(config_path):
            os.makedirs(config_path)
        config_file = config_path + CONFIG_FILE
        db_url = 'sqlite:///' + config_path + "/sqlite.db"
        if os.path.isfile(config_file):
            raise Exception(f"file {config_file} already exists")
        with open(config_file, "w") as f:
            f.write("[DEFAULT]\n")
            f.write("DatabaseUrl = " + db_url + "\n")
        logger.info(f"file {config_file}  created")
        return Config(config_path=config_path)

    def _read(self, key):
        config_file = self.config_path + CONFIG_FILE
        if not os.path.isfile(config_file):
            raise Exception(f"file {config_file} does not exist")
        parser = configparser.ConfigParser()
        logger.debug(f"reading key {key}")
        parser.read(config_file)
        value = parser['DEFAULT'].get(key)
        if not value:
            raise Exception(f"file {config_file} does not contain key {key}")
        return value
