# -*- coding: utf-8 -*-

import unittest
import os
import logging.config

from config import Config
from datamodel import User
from status import Status
from user_service import UserService

logging.config.fileConfig('logging_test.ini', disable_existing_loggers=False)

TEST_PATH = os.path.abspath(os.getcwd() + "/../target/")
TEST_PUBKEY = "MEgCQQChLLM582ZAE+rSsDimhXbln+8jCY5gDeyNGdgIK5crhIU3kiRJWr6V711Or2AmtMBHHoFf1rz1Mbjw+YOn4x5JAgMBAAE="
TEST_UID = "8a88e12a-98d6-4c1c-9850-d3cf5b31ca8a"


class TestUser(unittest.TestCase):

    def setUp(self):
        Config(path=TEST_PATH, dbtype='memory', rsabits=256)

    def test1_register(self):
        service = UserService()
        owner = service.register()
        self.assertEqual(User, type(owner ))
        self.assertEqual(owner , service.registered())
        duplicate = service.register(name="mickael")
        self.assertEqual(None, duplicate)
        self.assertEqual("Owner is already registered", Status.errormsg())

    def test2_add_list(self):
        service = UserService()
        user = service.add(TEST_UID, "testuser", "test@email.org", TEST_PUBKEY)
        self.assertEqual(User, type(user))
        self.assertIn(user, service.list())
        duplicate = service.add(TEST_UID, "otheruser", "other@email.org", TEST_PUBKEY)
        self.assertEqual(None, duplicate)
        self.assertEqual("IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: users.uid",
                         Status.errormsg())

    def test3_add_badkey(self):
        service = UserService()
        user = service.add(TEST_UID, "otheruser", "other@email.org", "bad key")
        self.assertEqual(None, user)
        self.assertEqual("Error: Incorrect padding", Status.errormsg())


if __name__ == '__main__':
    unittest.main()
