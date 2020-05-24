# -*- coding: utf-8 -*-

import logging.config
import os
import unittest
import uuid
from unittest.mock import MagicMock, patch, PropertyMock

from pysds.config import Config
from pysds.datamodel import Token, User, Dataset
from pysds.token_service import TokenService

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_UUID = "f6f8f779-e2f9-4fb5-8021-eabfa9248ade"
TEST_PUBKEY = "MEgCQQCm0wfw5h/TYrRJwk0L4UPR7ZgGpswAxMS3V86vhzLA69WRnZzNJ24Wphw5/Yseb4E60Vzp0dW4elkuFR5N+R8TAgMBAAE="

lastuid = None


class TestTokenService(unittest.TestCase):
    service: TokenService = None
    dsuid = uuid.uuid4()

    @classmethod
    def setUpClass(cls) -> None:
        logging.config.fileConfig(os.path.dirname(__file__) + "/logging_test.ini", disable_existing_loggers=False)
        Config(db_url='sqlite:///:memory:', key_length=512)
        cls.service = TokenService()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.service.database.close()
        Config.destroy()

    @patch('pysds.user_service.UserService.admin', PropertyMock(return_value=User(uid=str(uuid.uuid4()))), create=True)
    @patch('pysds.dataset_service.DatasetService.find', MagicMock(return_value=Dataset(uid=str(dsuid))))
    def test_request(self):
        token = self.service.create(self.dsuid)
        self.assertEqual(Token, type(token))

