# -*- coding: utf-8 -*-
import logging.config
import os
import unittest

from pysds.config import Config, CONFIG_FILE

TEST_CFG_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../target/")
TEST_CFG_FILE = TEST_CFG_PATH + CONFIG_FILE


class TestConfig(unittest.TestCase):

    def setUp(self):
        logging.config.fileConfig(os.path.dirname(__file__) + "/logging_test.ini", disable_existing_loggers=False)
        Config.destroy()

    def test_create(self):
        self.cleanup()
        config = Config.create(config_path=TEST_CFG_PATH)
        self.assertTrue(os.path.isfile(TEST_CFG_FILE))

    def test_get_url(self):
        config = Config(config_path=TEST_CFG_PATH)
        self.assertEqual("sqlite:///" + TEST_CFG_PATH + "/sqlite.db", config.db_url)

    def test_set_url(self):
        config = Config(config_path=TEST_CFG_PATH, db_url='sqlite:///:memory:')
        self.assertEqual('sqlite:///:memory:', config.db_url)

    def test_xception_no_config_file(self):
        self.cleanup()
        with self.assertRaises(Exception) as error:
            Config(config_path=TEST_CFG_PATH)
        self.assertEqual(f"file {TEST_CFG_FILE} does not exist", str(error.exception))

    def test_xception_no_property(self):
        self.cleanup()
        with open(TEST_CFG_FILE, "w") as f:
            f.write("[DEFAULT]\n")
        with self.assertRaises(Exception) as error:
            Config(config_path=TEST_CFG_PATH)
        self.assertEqual(f"file {TEST_CFG_FILE} does not contain key DatabaseUrl", str(error.exception))

    @staticmethod
    def cleanup():
        if os.path.exists(TEST_CFG_FILE):
            os.remove(TEST_CFG_FILE)
