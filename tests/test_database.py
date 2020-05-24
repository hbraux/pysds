# -*- coding: utf-8 -*-
import logging.config
import os
import shutil
import sys
import unittest

from sqlalchemy import Column, Integer

from pysds.config import Config
from pysds.database import Database, Base

sys.path.append(os.path.dirname(__file__))


TEST_CFG_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../target/")


class DatabaseSample(Base):
    __tablename__ = 'database_sample'
    sid = Column(Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return f"DatabaseSample({self.sid})"


class TestDatabase(unittest.TestCase):

    def setUp(self):
        logging.config.fileConfig(os.path.dirname(__file__) + "/logging_test.ini", disable_existing_loggers=False)

    def tearDown(self) -> None:
        self.db.close()
        Database.destroy()
        Config.destroy()

    def test_db(self):
        Config(db_url='sqlite:///:memory:')
        self.db = Database()
        obj = DatabaseSample()
        self.db.add(obj)
        self.assertEqual(obj, self.db.get(DatabaseSample, DatabaseSample.sid == 1))
        self.assertEqual([obj], self.db.list(DatabaseSample))

    def test_xception_no_schema(self):
        if os.path.exists(TEST_CFG_PATH):
            shutil.rmtree(TEST_CFG_PATH)
        Config.create(config_path=TEST_CFG_PATH)
        self.db = Database()
        obj = DatabaseSample()
        with self.assertRaises(Exception) as error:
            self.db.add(obj)
        self.assertEqual("(sqlite3.OperationalError) no such table: database_sample",
                         str(error.exception).splitlines()[0])

