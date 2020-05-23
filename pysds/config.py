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
        self._config_path = config_path
        self.key_length = key_length
        self._db_url = db_url

    def db_url(self) -> str:
        if not self._db_url:
            self._db_url = self._read('DatabaseUrl')
        return self._db_url

    def create(self) -> None:
        if not os.path.isdir(self._config_path):
            os.makedirs(self._config_path)
        cfgfile = self._config_path + CONFIG_FILE
        dburl = 'sqlite:///' + self._config_path + "/sqlite.db"
        if os.path.isfile(cfgfile):
            raise Exception(f"file {cfgfile} already exists")
        with open(cfgfile, "w") as f:
            f.write("[DEFAULT]\n")
            f.write("DatabaseUrl = " + dburl + "\n")
        logger.info(f"file {cfgfile}  created")

    def _read(self, key):
        cfgfile = self._config_path + CONFIG_FILE
        if not os.path.isfile(cfgfile):
            raise Exception(f"file {cfgfile} does not exist")
        parser = configparser.ConfigParser()
        logger.debug(f"reading key {key}")
        parser.read(cfgfile)
        value = parser['DEFAULT'].get(key)
        if not value:
            raise Exception(f"file {cfgfile} does not contain key {key}")
        return value
