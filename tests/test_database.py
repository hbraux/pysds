# -*- coding: utf-8 -*-
import logging.config
import os
import sys
import unittest

from pysds.config import Config
from pysds.database import Database

sys.path.insert(0, os.path.dirname(__file__))

from database_sample import DatabaseSample


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.config.fileConfig(os.path.dirname(__file__) + "/logging_test.ini", disable_existing_loggers=False)
        Config(db_url='sqlite:///:memory:')

    def test_db(self):
        db = Database()
        obj = DatabaseSample()
        db.add(obj)
        self.assertEqual(obj, db.get(DatabaseSample, DatabaseSample.sid == 1))
        self.assertEqual([obj], db.list(DatabaseSample))
