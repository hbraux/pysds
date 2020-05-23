# -*- coding: utf-8 -*-
import logging.config
import os
import sys
import unittest

from pysds.config import Config
from pysds.database import Database

sys.path.insert(0, os.path.dirname(__file__))

from database_sample import DatabaseSample

TEST_CFG_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../target/")


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.config.fileConfig(os.path.dirname(__file__) + "/logging_test.ini", disable_existing_loggers=False)

    def test_db(self):
        Config.destroy()
        Config(db_url='sqlite:///:memory:')
        db = Database()
        obj = DatabaseSample()
        db.add(obj)
        self.assertEqual(obj, db.get(DatabaseSample, DatabaseSample.sid == 1))
        self.assertEqual([obj], db.list(DatabaseSample))

    def test__exception_no_schema(self):
        Config.destroy()
        Config(config_path=TEST_CFG_PATH, db_url=None)
        db = Database()
        obj = DatabaseSample()
        self.assertRaises(Exception, db.add, obj)


