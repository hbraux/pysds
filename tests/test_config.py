# -*- coding: utf-8 -*-
import logging.config
import os
import shutil
import unittest

from config import Config, CONFIG_FILE
from status import Status

TEST_CFG_PATH = os.path.abspath(os.getcwd() + "/../target/")
TEST_CFG_FILE = TEST_CFG_PATH + "/" + CONFIG_FILE
TEST_DB_URL = "sqlite:///" + TEST_CFG_PATH + "/sqlite.db"
TEST_MEM_URL = "sqlite:///:memory:"

CONFIG_4TEST = Config(cfgpath=TEST_CFG_PATH, dburl=TEST_MEM_URL, keylen=256)


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.do_clean()
        logging.config.fileConfig('logging_test.ini', disable_existing_loggers=False)

    def test_create(self):
        config = Config(cfgpath=TEST_CFG_PATH)
        config.create()
        self.assertTrue(os.path.isfile(TEST_CFG_FILE))
        self.assertEqual(TEST_DB_URL, config.dburl)
        self.assertEqual(TEST_DB_URL, config.read('DatabaseUrl'))
        config.create()
        self.assertEqual("config already initialized", Status.errormsg())

    def test_create_with_url(self):
        config = CONFIG_4TEST
        config.create()
        self.assertTrue(os.path.isfile(TEST_CFG_FILE))
        self.assertEqual(TEST_MEM_URL, config.dburl)
        self.assertEqual(TEST_MEM_URL, config.read('DatabaseUrl'))

    @staticmethod
    def do_clean():
        if os.path.isdir(TEST_CFG_PATH):
            shutil.rmtree(TEST_CFG_PATH)



