# -*- coding: utf-8 -*-

"""Application Configuration"""

import os

from singleton import Singleton


class Config(metaclass=Singleton):

    def __init__(self, path='~/.sds', dbtype='sqlite', rsabits=2048):
        self.path = os.path.expanduser(path)
        self.dbtype = dbtype
        self.rsabits = rsabits
