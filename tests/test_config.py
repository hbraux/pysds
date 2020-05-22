# -*- coding: utf-8 -*-
import logging.config
import os
import unittest

from pysds.config import Config, CONFIG_FILE

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_CFG_PATH = os.path.abspath(ROOT_DIR + "/../target/")
TEST_DB_URL = "sqlite:///" + TEST_CFG_PATH + "/sqlite.db"
TEST_MEM_URL = 'sqlite:///:memory:'


class TestConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.config.fileConfig(ROOT_DIR + "/logging_test.ini", disable_existing_loggers=False)

    def test_create(self):
        Config.destroy()
        config = Config.create(cfgpath=TEST_CFG_PATH)
        self.assertEqual(Config, type(config))
        self.assertTrue(os.path.isfile(TEST_CFG_PATH + CONFIG_FILE))
        self.assertEqual(TEST_DB_URL, config.dburl)

    def test_init(self):
        Config.destroy()
        config = Config(cfgpath=TEST_CFG_PATH)
        self.assertEqual(TEST_DB_URL, config.dburl)

    def test_url(self):
        Config.destroy()
        config = Config(cfgpath=TEST_CFG_PATH, dburl=TEST_MEM_URL)
        self.assertEqual(TEST_MEM_URL, config.dburl)
