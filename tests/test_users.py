# -*- coding: utf-8 -*-
import logging.config
import os
import unittest
import uuid

from injector import Injector

from pysyd.config import Config
from pysyd.datamodel import User
from pysyd.services import UserService
from test_config import config4test

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestUsers(unittest.TestCase):

    def setUp(self):
        logging.config.fileConfig(ROOT_DIR + "/logging_test.ini", disable_existing_loggers=False)
        injector = Injector()
        injector.binder.bind(Config, to=config4test())
        self.service = injector.get(UserService)

    def test_admin(self):
        self.assertIsNotNone(self.service.admin)

    def test_add_list(self):
        testuid = uuid.uuid4()
        pubkey = "MEgCQQChLLM582ZAE+rSsDimhXbln+8jCY5gDeyNGdgIK5crhIU3kiRJWr6V711Or2AmtMBHHoFf1rz1Mbjw+YOn4x5JAgMBAAE="
        user = self.service.add(testuid, "testuser", "test@email.org", pubkey)
        self.assertEqual(User, type(user))
        self.assertIn(user, self.service.list())
        duplicate = self.service.add(testuid, "otheruser", "other@email.org", pubkey)
        self.assertEqual(None, duplicate)
        self.assertEqual("IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: users.uid",
                         self.service.errormsg())

    def test_add_badkey(self):
        testuid = uuid.uuid4()
        user = self.service.add(testuid, "otheruser", "other@email.org", "bad key")
        self.assertEqual(None, user)
        self.assertEqual("Error: Incorrect padding", self.service.errormsg())


