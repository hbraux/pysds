# -*- coding: utf-8 -*-
import logging.config
import os
import unittest

from database_sample import DatabaseSample
from pysds.database import Database
from test_config import TestConfig

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestDatabase(unittest.TestCase):

    def setUp(self):
        logging.config.fileConfig(ROOT_DIR + "/logging_test.ini", disable_existing_loggers=False)

    def test(self):
        TestConfig.use()
        db = Database()
        obj = DatabaseSample()
        db.add(obj)
        self.assertEqual(obj, db.get(DatabaseSample, DatabaseSample.sid == 1))
        self.assertEqual([obj], db.list(DatabaseSample))
