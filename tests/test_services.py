# -*- coding: utf-8 -*-
import os
import unittest
import logging.config

from injector import Injector

from pysds.config import Config
from pysds.datamodel import User
from pysds.services import UserService
from test_config import config4test

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_PUBKEY = "MEgCQQChLLM582ZAE+rSsDimhXbln+8jCY5gDeyNGdgIK5crhIU3kiRJWr6V711Or2AmtMBHHoFf1rz1Mbjw+YOn4x5JAgMBAAE="
TEST_UID = "8a88e12a-98d6-4c1c-9850-d3cf5b31ca8a"


class TestUser(unittest.TestCase):

    def setUp(self):
        logging.config.fileConfig(ROOT_DIR + "/logging_test.ini", disable_existing_loggers=False)
        injector = Injector()
        injector.binder.bind(Config, to=config4test())
        self.service = injector.get(UserService)

    def test_create_admin(self):
        self.service.create_admin()
        self.assertEqual(User, type(self.service.admin))

    def test_add_list(self):
        user = self.service.add(TEST_UID, "testuser", "test@email.org", TEST_PUBKEY)
        self.assertEqual(User, type(user))
        self.assertIn(user, self.service.list())
        duplicate = self.service.add(TEST_UID, "otheruser", "other@email.org", TEST_PUBKEY)
        self.assertEqual(None, duplicate)
        self.assertEqual("IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: users.uid",
                         self.service.errormsg())

    def test_add_badkey(self):
        user = self.service.add(TEST_UID, "otheruser", "other@email.org", "bad key")
        self.assertEqual(None, user)
        self.assertEqual("Error: Incorrect padding", self.service.errormsg())


