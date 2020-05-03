# -*- coding: utf-8 -*-

import unittest
import os
import logging.config
import uuid

from config import Config
from status import Status
from user_service import UserService

logging.config.fileConfig('logging_test.ini', disable_existing_loggers=False)

TEST_PATH = os.path.abspath(os.getcwd() + "/../target/")
TEST_PUBKEY = "MEgCQQChLLM582ZAE+rSsDimhXbln+8jCY5gDeyNGdgIK5crhIU3kiRJWr6V711Or2AmtMBHHoFf1rz1Mbjw+YOn4x5JAgMBAAE="
TEST_UID = "8a88e12a-98d6-4c1c-9850-d3cf5b31ca8a"


class TestUser(unittest.TestCase):

    def setUp(self):
        cfg = Config(path=TEST_PATH, dbtype='memory', rsabits=256)
        self.service = UserService()

    def test_set_owner(self):
        owner = self.service.set_owner()
        self.assertEqual(True, self.owner is not None)
        self.assertEqual(owner, self.service.get_owner())

    def test_set_owner_dup(self):
        self.assertEqual(None, self.service.set_owner(name="mickael"))
        self.assertEqual("IntegrityError:", Status.msg())

    def test_register(self):
        self.assertEqual(True, self.service.add(TEST_UID, "testuser", "test@email.org", TEST_PUBKEY))

    def test_register_duplicate(self):
        self.assertEqual(False, self.service.add(TEST_UID, "otheruser", "other@email.org", TEST_PUBKEY))
        self.assertEqual("IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: users.uid",
                         Status.msg())

    def test_register_badkey(self):
        self.assertEqual(False, self.service.add(str(uuid.uuid4()), "otheruser", "other@email.org", "hello"))
        self.assertEqual("Error: Incorrect padding", Status.msg())


if __name__ == '__main__':
    unittest.main()
