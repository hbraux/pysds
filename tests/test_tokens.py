# -*- coding: utf-8 -*-

import logging.config
import os
import unittest

from injector import Injector

from pysds.config import Config
from pysds.datamodel import Token
from pysds.services import TokenService
from test_config import config4test

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_UUID = "f6f8f779-e2f9-4fb5-8021-eabfa9248ade"
TEST_PUBKEY = "MEgCQQCm0wfw5h/TYrRJwk0L4UPR7ZgGpswAxMS3V86vhzLA69WRnZzNJ24Wphw5/Yseb4E60Vzp0dW4elkuFR5N+R8TAgMBAAE="

lastuid = None


class TestToken(unittest.TestCase):
    service: TokenService = None
    dsuid = None

    @classmethod
    def setUpClass(cls) -> None:
        logging.config.fileConfig(ROOT_DIR + "/logging_test.ini", disable_existing_loggers=False)
        injector = Injector()
        injector.binder.bind(Config, to=config4test())
        cls.service = injector.get(TokenService)
        cls.service.datasetservice.userservice.add(TEST_UUID, "testuser", "test@email.org", TEST_PUBKEY)
        cls.dsuid = cls.service.datasetservice.load(ROOT_DIR + "/wires.sds_").uid

    def test_request(self):
        token = self.service.create(self.dsuid)
        self.assertEqual(Token, type(token))

