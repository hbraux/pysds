# -*- coding: utf-8 -*-

"""Application Configuration"""
import configparser
import logging
import os

# Default configuration values
from status import Status

CONFIG_PATH = os.path.expanduser(os.getenv('SDS_CONFIG_PATH', '~/.sds'))
CONFIG_FILE = "sds.ini"

logger = logging.getLogger(__name__)


class Config:
    def __init__(self, cfgpath=CONFIG_PATH, keylen=2048, dburl=None):
        self.cfgpath = cfgpath
        self.cfgfile = cfgpath + "/" + CONFIG_FILE
        self.keylen = keylen
        self.dburl = dburl or self.read('DatabaseUrl')

    def read(self, key):
        logger.debug("reading key %s", key)
        parser = configparser.ConfigParser()
        if not os.path.isfile(self.cfgfile):
            return None
        parser.read(self.cfgfile)
        return parser['DEFAULT'].get(key)

    def create(self):
        if not os.path.isdir(self.cfgpath):
            os.makedirs(self.cfgpath)
        if os.path.isfile(self.cfgfile):
            logger.error("file %s already exists", self.cfgfile)
            Status.failed("config already initialized")
            return
        if not self.dburl:
            self.dburl = 'sqlite:///' + self.cfgpath + "/sqlite.db"
        with open(self.cfgfile, "w") as f:
            f.write("[DEFAULT]\n")
            f.write("DatabaseUrl = " + self.dburl + "\n")
        logger.info("file %s created", self.cfgfile)





