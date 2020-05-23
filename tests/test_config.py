# -*- coding: utf-8 -*-
import logging.config
import os
import unittest

from pysds.config import Config, CONFIG_FILE

TEST_CFG_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../target/")


class TestConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.config.fileConfig(os.path.dirname(__file__) + "/logging_test.ini", disable_existing_loggers=False)
        Config.destroy()

    def test_create(self):
        self.cleanup()
        Config.destroy()
        config = Config(config_path=TEST_CFG_PATH)
        config.create()
        self.assertTrue(os.path.isfile(TEST_CFG_PATH + CONFIG_FILE))

    def test_read_conf(self):
        Config.destroy()
        config = Config(config_path=TEST_CFG_PATH)
        self.assertEqual("sqlite:///" + TEST_CFG_PATH + "/sqlite.db", config.db_url())

    def test_set_url(self):
        Config.destroy()
        config = Config(config_path=TEST_CFG_PATH, db_url='sqlite:///:memory:')
        self.assertEqual('sqlite:///:memory:', config.db_url())

    @staticmethod
    def cleanup():
        if os.path.exists(TEST_CFG_PATH + CONFIG_FILE):
            os.remove(TEST_CFG_PATH + CONFIG_FILE)
