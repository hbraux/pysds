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

    def __init__(self, cfgpath=CONFIG_PATH, keylen=DEFAULT_KEY_LEN, dburl=None):
        self.cfgpath = cfgpath
        self.keylen = keylen
        self.dburl = dburl or self._read('DatabaseUrl')

    def _read(self, key):
        parser = configparser.ConfigParser()
        logger.debug("reading key %s ", key,)
        parser.read(self.cfgpath + CONFIG_FILE)
        return parser['DEFAULT'].get(key)

    @staticmethod
    def create(cfgpath=CONFIG_PATH, dburl=None, clean=True):
        if not os.path.isdir(cfgpath):
            os.makedirs(cfgpath)
        cfgfile = cfgpath + CONFIG_FILE
        dburl = dburl or 'sqlite:///' + cfgpath + "/sqlite.db"
        if os.path.isfile(cfgfile):
            if clean:
                logger.warning(f"file {cfgfile} already exists and will be overriden")
            else:
                raise Exception(f"file {cfgfile} already exists")
        with open(cfgfile, "w") as f:
            f.write("[DEFAULT]\n")
            f.write("DatabaseUrl = " + dburl + "\n")
        logger.info("file %s created", cfgfile)
        return Config(cfgpath=cfgpath, dburl=dburl)


