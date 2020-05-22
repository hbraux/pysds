# -*- coding: utf-8 -*-

import logging.config
import os
import unittest
import uuid

from pysds.config import Config
from pysds.datamodel import Dataset
from pysds.dataset_service import DatasetService
from pysds.user_service import UserService

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_UUID = "f6f8f779-e2f9-4fb5-8021-eabfa9248ade"
TEST_PUBKEY = "MEgCQQCm0wfw5h/TYrRJwk0L4UPR7ZgGpswAxMS3V86vhzLA69WRnZzNJ24Wphw5/Yseb4E60Vzp0dW4elkuFR5N+R8TAgMBAAE="
TEST_CFG_PATH = os.path.abspath(ROOT_DIR + "/../target/")

lastuid = None


class TestDatasetService(unittest.TestCase):
    service: DatasetService = None

    @classmethod
    def setUpClass(cls) -> None:
        logging.config.fileConfig(ROOT_DIR + "/logging_test.ini", disable_existing_loggers=False)
        Config.create(cfgpath=TEST_CFG_PATH, clean=True, dburl='sqlite:///:memory:')
        UserService.init().add(uuid.UUID(TEST_UUID), "testuser", "test@email.org", TEST_PUBKEY)
        cls.service = DatasetService()

    def test_import_csv(self):
        csvfile = ROOT_DIR + "/wires.csv"
        ds = self.service.imp("test", csvfile, {}, ignore=True)
        self.assertEqual(Dataset, type(ds))
        self.assertTrue(os.path.isfile(ROOT_DIR + "/wires.sds"))
        self.assertEqual(ds.owner, Dataset.OWNED)

    def test_load(self):
        global lastuid
        sdsfile = ROOT_DIR + "/wires.sds_"
        ds = self.service.load(sdsfile)
        self.assertEqual(Dataset, type(ds))
        self.assertNotEqual(ds.owner, Dataset.OWNED)
        lastuid = ds.uid

    def test_load_exists(self):
        sdsfile = ROOT_DIR + "/wires.sds_"
        self.assertIsNone(self.service.load(sdsfile))
        self.assertTrue(self.service.failure())
        self.assertEqual(f"Dataset {lastuid} already in local store", self.service.errormsg())

    def test_load_failure(self):
        sdsfile = __file__
        self.assertIsNone(self.service.load(sdsfile))
        self.assertTrue(self.service.failure())
        self.assertEqual(f"{sdsfile} is not a DataSet file", self.service.errormsg())
