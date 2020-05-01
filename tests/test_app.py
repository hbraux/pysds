# -*- coding: utf-8 -*-

import unittest
import os
import shutil
import logging.config
import uuid
from sqlite3 import IntegrityError

from pysds.app import App

logging.config.fileConfig('logging_test.ini', disable_existing_loggers=False)

TEST_PATH = os.path.abspath(os.getcwd() + "/../target/")
TEST_PUBKEY = "MEgCQQChLLM582ZAE+rSsDimhXbln+8jCY5gDeyNGdgIK5crhIU3kiRJWr6V711Or2AmtMBHHoFf1rz1Mbjw+YOn4x5JAgMBAAE="
TEST_UID = "8a88e12a-98d6-4c1c-9850-d3cf5b31ca8a"
class TestApp(unittest.TestCase):

    def test_setup_memory(self):
        cleanup()
        app = App(path=TEST_PATH, dbtype='memory', rsabits=256)
        self.assertFalse(app.open())
        app.setup()
        self.assertTrue(app.open())

    def test_setup_file(self):
        cleanup()
        app = App(path=TEST_PATH, rsabits=256)
        self.assertFalse(app.open())
        app.setup()
        self.assertTrue(app.open())

    def test_register(self):
        app = App(path=TEST_PATH)
        app.open()
        app.register(TEST_UID, "testuser","test@email.org", TEST_PUBKEY)

    def test_register_duplicate(self):
        app = App(path=TEST_PATH)
        app.open()
        self.assertRaises(Exception, app.register, TEST_UID, "otheruser","other@email.org", TEST_PUBKEY)

    def test_register_badkey(self):
        app = App(path=TEST_PATH)
        app.open()
        self.assertRaises(Exception, app.register, str(uuid.uuid4()), "otheruser","other@email.org", "hello")

def cleanup():
    if os.path.isdir(TEST_PATH):
        shutil.rmtree(TEST_PATH)


