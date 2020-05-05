# -*- coding: utf-8 -*-

"""Application Configuration"""

import os

CONFIG_PATH = os.getenv('SDS_CONFIG_PATH', '~/.sds')
CONFIG_FILE = "sds.ini"
CONFIG_URL = 'sqlite:///' + CONFIG_PATH + "/sqlite.db"


class Config:
    def __init__(self, path='~/.sds', dbtype='sqlite', rsabits=2048):
        self.path = os.path.expanduser(path)
        self.dbtype = dbtype
        self.rsabits = rsabits

    @staticmethod
    def test():
        return Config(path=os.path.abspath(os.getcwd() + "/../target/"), dbtype='memory', rsabits=256)

