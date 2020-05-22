# -*- coding: utf-8 -*-
import logging.config
import os
import unittest

from database_sample import DatabaseSample
from pysds.config import Config
from pysds.database import Database

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_CFG_PATH = os.path.abspath(ROOT_DIR + "/../target/")


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.config.fileConfig(ROOT_DIR + "/logging_test.ini", disable_existing_loggers=False)
        if os.path.isfile(TEST_CFG_PATH + "/sqlite.db"):
            os.remove(TEST_CFG_PATH + "/sqlite.db")
        Config.create(cfgpath=TEST_CFG_PATH, clean=True)

    def test_create(self):
        db = Database.create()
        self.assertEqual(Database, type(db))

    def test_db(self):
        db = Database()
        obj = DatabaseSample()
        db.add(obj)
        self.assertEqual(obj, db.get(DatabaseSample, DatabaseSample.sid == 1))
        self.assertEqual([obj], db.list(DatabaseSample))

