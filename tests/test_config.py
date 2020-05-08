# -*- coding: utf-8 -*-
import logging.config
import os
import shutil
import unittest

from config import Config, CONFIG_FILE

TEST_CFG_PATH = os.path.abspath(os.getcwd() + "/../target/")
TEST_DB_URL = "sqlite:///" + TEST_CFG_PATH + "/sqlite.db"
TEST_MEM_URL = 'sqlite:///:memory:'


class TestConfig(unittest.TestCase):

    def setUp(self):
        logging.config.fileConfig('logging_test.ini', disable_existing_loggers=False)

    def test_init(self):
        self.do_clean()
        config = Config(cfgpath=TEST_CFG_PATH, init=True)
        self.assertTrue(os.path.isfile(TEST_CFG_PATH + CONFIG_FILE))
        self.assertEqual(TEST_DB_URL, config.dburl)

    def test_no_init(self):
        config = Config(cfgpath=TEST_CFG_PATH)
        self.assertEqual(TEST_DB_URL, config.dburl)

    def test_url(self):
        config = Config(cfgpath=TEST_CFG_PATH, dburl=TEST_MEM_URL)
        self.assertEqual(TEST_MEM_URL, config.dburl)

    @staticmethod
    def do_clean():
        if os.path.isdir(TEST_CFG_PATH):
            shutil.rmtree(TEST_CFG_PATH)


def config4test():
    return Config(cfgpath=TEST_CFG_PATH, dburl=TEST_MEM_URL, keylen=256, init=True)

