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


class TestDatasets(unittest.TestCase):

    def setUp(self):
        logging.config.fileConfig(ROOT_DIR + "/logging_test.ini", disable_existing_loggers=False)
        injector = Injector()
        injector.binder.bind(Config, to=config4test())
        self.service = injector.get(DatasetService)

    def test_add_csv(self):
        csvfile = ROOT_DIR + "/wires.csv"
        ds = self.service.add("test", open(csvfile))
        self.assertEqual(Dataset, type(ds))

