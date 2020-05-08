import unittest
import logging.config
import logging
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class TestTokens(unittest.TestCase):

    def setUp(self):
        logging.config.fileConfig(ROOT_DIR + "/logging_test.ini", disable_existing_loggers=False)

    def test_create(self):
        self.assertTrue(True)



