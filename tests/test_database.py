# -*- coding: utf-8 -*-
import logging.config
import os
import unittest

from injector import Injector

from pysds.config import Config
from pysds.database import Database
from sample import Sample
from test_config import config4test

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestDatabase(unittest.TestCase):

    def setUp(self):
        logging.config.fileConfig(ROOT_DIR + "/logging_test.ini", disable_existing_loggers=False)

    def test(self):
        injector = Injector()
        injector.binder.bind(Config, to=config4test())
        db = injector.get(Database)
        obj = Sample()
        db.add(obj)
        self.assertEqual(obj, db.get(Sample, Sample.sid == 1))
        self.assertEqual([obj], db.list(Sample))
