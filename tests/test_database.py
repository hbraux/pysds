# -*- coding: utf-8 -*-
import logging.config
import unittest

from injector import Injector

from config import Config
from database import Database
from test_config import CONFIG_4TEST
from test_sample import Sample


class TestDatabase(unittest.TestCase):

    def setUp(self):
        logging.config.fileConfig('logging_test.ini', disable_existing_loggers=False)
        injector = Injector()
        injector.binder.bind(Config, to=CONFIG_4TEST)
        self.db: Database = injector.get(Database)

    def test(self):
        self.db.create()
        obj = Sample(msg="hello")
        self.db.add(obj)
        self.assertEqual(obj, self.db.get(Sample, Sample.msg == "hello"))
        self.assertEqual([obj], self.db.list(Sample))

