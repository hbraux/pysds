# -*- coding: utf-8 -*-
import os
import unittest
import logging.config
import uuid

from injector import Injector

from pysds.config import Config
from pysds.datamodel import User, Dataset
from pysds.services import UserService, DatasetService
from test_config import config4test

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestUser(unittest.TestCase):

    def setUp(self):
        logging.config.fileConfig(ROOT_DIR + "/logging_test.ini", disable_existing_loggers=False)
        injector = Injector()
        injector.binder.bind(Config, to=config4test())
        self.service = injector.get(UserService)

    def test_admin(self):
        self.assertIsNotNone(self.service.admin)

    def test_add_list(self):
        testuid = str(uuid.uuid4())
        pubkey = "MEgCQQChLLM582ZAE+rSsDimhXbln+8jCY5gDeyNGdgIK5crhIU3kiRJWr6V711Or2AmtMBHHoFf1rz1Mbjw+YOn4x5JAgMBAAE="
        user = self.service.add(testuid, "testuser", "test@email.org", pubkey)
        self.assertEqual(User, type(user))
        self.assertIn(user, self.service.list())
        duplicate = self.service.add(testuid, "otheruser", "other@email.org", pubkey)
        self.assertEqual(None, duplicate)
        self.assertEqual("IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: users.uid",
                         self.service.errormsg())

    def test_add_badkey(self):
        testuid = str(uuid.uuid4())
        user = self.service.add(testuid, "otheruser", "other@email.org", "bad key")
        self.assertEqual(None, user)
        self.assertEqual("Error: Incorrect padding", self.service.errormsg())

    def test_add_baduid(self):
        testuid = 'e0e68196-375b-4078-a34-f8de4b406276'
        user = self.service.add(testuid, "otheruser", "other@email.org", "bad key")
        self.assertEqual(None, user)
        self.assertEqual("ValueError: badly formed hexadecimal UUID string", self.service.errormsg())


class TestDataset(unittest.TestCase):

    def setUp(self):
        logging.config.fileConfig(ROOT_DIR + "/logging_test.ini", disable_existing_loggers=False)
        injector = Injector()
        injector.binder.bind(Config, to=config4test())
        self.service = injector.get(DatasetService)

    def test_add_csv(self):
        csvfile = "wires.csv"
        ds = self.service.add("test", open(csvfile))
        self.assertEqual(Dataset, type(ds))

