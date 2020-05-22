# -*- coding: utf-8 -*-
import logging.config
import os
import unittest
import uuid

from pysds.config import Config
from pysds.datamodel import User
from pysds.user_service import UserService

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_CFG_PATH = os.path.abspath(ROOT_DIR + "/../target/")


class TestUserService(unittest.TestCase):
    service: UserService = None

    @classmethod
    def setUpClass(cls):
        logging.config.fileConfig(ROOT_DIR + "/logging_test.ini", disable_existing_loggers=False)
        Config.create(cfgpath=TEST_CFG_PATH, clean=True, dburl='sqlite:///:memory:')
        cls.service = UserService.init()

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
