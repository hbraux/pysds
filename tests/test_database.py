# -*- coding: utf-8 -*-
import logging.config
import unittest

from injector import Injector

from config import Config
from database import Database
from test_config import config4test
from test_sample import Sample


class TestDatabase(unittest.TestCase):

    def setUp(self):
        logging.config.fileConfig('logging_test.ini', disable_existing_loggers=False)

    def test(self):
        injector = Injector()
        injector.binder.bind(Config, to=config4test())
        db = injector.get(Database)
        obj = Sample()
        db.add(obj)
        self.assertEqual(obj, db.get(Sample, Sample.sid == 1))
        self.assertEqual([obj], db.list(Sample))

