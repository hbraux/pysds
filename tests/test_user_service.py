# -*- coding: utf-8 -*-
import logging.config
import os
import unittest
import uuid

from pysds.config import Config
from pysds.datamodel import User
from pysds.user_service import UserService


class TestUserService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.config.fileConfig(os.path.dirname(__file__) + "/logging_test.ini", disable_existing_loggers=False)

    def setUp(self) -> None:
        Config(db_url='sqlite:///:memory:', key_length=512)
        self.service = UserService()

    def test_admin(self):
        admin = self.service.create_admin()
        self.assertIsNotNone(admin)
        self.assertEqual(admin, self.service.admin())
        self.assertTrue(admin.is_admin)

    def test_user_add(self):
        testuid = uuid.uuid4()
        pubkey = "MEgCQQChLLM582ZAE+rSsDimhXbln+8jCY5gDeyNGdgIK5crhIU3kiRJWr6V711Or2AmtMBHHoFf1rz1Mbjw+YOn4x5JAgMBAAE="
        user = self.service.add(testuid, "testuser", "test@email.org", pubkey)
        self.assertEqual(User, type(user))
        self.assertIn(user, self.service.list())
        self.assertEqual(user, self.service.find(testuid))
        duplicate = self.service.add(testuid, "otheruser", "other@email.org", pubkey)
        self.assertEqual(None, duplicate)
        self.assertEqual("IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: users.uid",
                         self.service.errormsg())

    def test_user_add_badkey(self):
        testuid = uuid.uuid4()
        user = self.service.add(testuid, "otheruser", "other@email.org", "bad key")
        self.assertEqual(None, user)
        self.assertEqual("Error: Incorrect padding", self.service.errormsg())
