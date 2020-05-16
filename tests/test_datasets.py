# -*- coding: utf-8 -*-

import logging.config
import os
import unittest

from injector import Injector

from pysds.config import Config
from pysds.datamodel import Dataset
from pysds.services import DatasetService
from test_config import config4test

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_UUID = "f6f8f779-e2f9-4fb5-8021-eabfa9248ade"
TEST_PUBKEY = "MEgCQQCm0wfw5h/TYrRJwk0L4UPR7ZgGpswAxMS3V86vhzLA69WRnZzNJ24Wphw5/Yseb4E60Vzp0dW4elkuFR5N+R8TAgMBAAE="

lastuid = None


class TestDatasets(unittest.TestCase):
    service: DatasetService = None

    @classmethod
    def setUpClass(cls) -> None:
        logging.config.fileConfig(ROOT_DIR + "/logging_test.ini", disable_existing_loggers=False)
        injector = Injector()
        injector.binder.bind(Config, to=config4test())
        cls.service = injector.get(DatasetService)
        cls.service.userservice.add(TEST_UUID, "testuser", "test@email.org", TEST_PUBKEY)

    def test_import_csv(self):
        csvfile = ROOT_DIR + "/wires.csv"
        ds = self.service.imp("test", csvfile, {}, ignore=True)
        self.assertEqual(Dataset, type(ds))
        self.assertTrue(os.path.isfile(ROOT_DIR + "/wires.sds"))
        self.assertEqual(ds.owner, DatasetService.OWNED)

    def test_load(self):
        global lastuid
        sdsfile = ROOT_DIR + "/wires.sds_"
        ds = self.service.load(sdsfile)
        self.assertEqual(Dataset, type(ds))
        self.assertNotEqual(ds.owner, DatasetService.OWNED)
        lastuid = ds.uid

    def test_load_exists(self):
        sdsfile = ROOT_DIR + "/wires.sds_"
        self.assertIsNone(self.service.load(sdsfile))
        self.assertTrue(self.service.failure())
        self.assertEqual(f"Dataset {lastuid} already in local store", self.service.errormsg())

    def test_load_failured(self):
        sdsfile = ROOT_DIR + "/sample.py"
        self.assertIsNone(self.service.load(sdsfile))
        self.assertTrue(self.service.failure())
        self.assertEqual(f"{sdsfile} is not a DataSet file", self.service.errormsg())