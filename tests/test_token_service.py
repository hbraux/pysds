# -*- coding: utf-8 -*-

import logging.config
import os
import unittest
import uuid

from pysds.config import Config
from pysds.datamodel import Token
from pysds.dataset_service import DatasetService
from pysds.token_service import TokenService
from pysds.user_service import UserService

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_UUID = "f6f8f779-e2f9-4fb5-8021-eabfa9248ade"
TEST_PUBKEY = "MEgCQQCm0wfw5h/TYrRJwk0L4UPR7ZgGpswAxMS3V86vhzLA69WRnZzNJ24Wphw5/Yseb4E60Vzp0dW4elkuFR5N+R8TAgMBAAE="

lastuid = None


class TestTokenService(unittest.TestCase):
    dsuid = None
    service: TokenService = None

    @classmethod
    def setUpClass(cls) -> None:
        logging.config.fileConfig(os.path.dirname(__file__) + "/logging_test.ini", disable_existing_loggers=False)
        Config(db_url='sqlite:///:memory:', key_length=512)
        UserService().add(uuid.UUID(TEST_UUID), "testuser", "test@email.org", TEST_PUBKEY)
        cls.dsuid = DatasetService().load(TEST_DIR + "/wires.sds_").uid
        cls.service = TokenService()

    def test_request(self):
        token = self.service.create(self.dsuid)
        self.assertEqual(Token, type(token))

