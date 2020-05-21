# -*- coding: utf-8 -*-

"""Application Configuration"""
import configparser
import logging
import os

from pysds.singleton import Singleton

CONFIG_PATH = os.path.expanduser(os.getenv('SDS_CONFIG_PATH', '~/.sds'))
CONFIG_FILE = "/sds.ini"
# TODO: temporary value
DEFAULT_KEY_LEN = 512

logger = logging.getLogger(__name__)


class Config(metaclass=Singleton):
    """This singleton handles application configuration"""

    def __init__(self, cfgpath=CONFIG_PATH, keylen=DEFAULT_KEY_LEN, setup=False, dburl=None):
        self.cfgpath = cfgpath
        self.keylen = keylen
        self.setup = setup
        if self.setup:
            self.dburl = dburl or 'sqlite:///' + self.cfgpath + "/sqlite.db"
            self._create()
        else:
            self.dburl = dburl or self._read('DatabaseUrl')

    def _read(self, key):
        parser = configparser.ConfigParser()
        logger.debug("reading key %s ", key,)
        parser.read(self.cfgpath + CONFIG_FILE)
        return parser['DEFAULT'].get(key)

    def _create(self):
        if not os.path.isdir(self.cfgpath):
            os.makedirs(self.cfgpath)
        cfgfile = self.cfgpath + CONFIG_FILE
        if os.path.isfile(cfgfile):
            logger.warning("file %s already exists", cfgfile)
            return
        with open(cfgfile, "w") as f:
            f.write("[DEFAULT]\n")
            f.write("DatabaseUrl = " + self.dburl + "\n")
        logger.info("file %s created", cfgfile)
