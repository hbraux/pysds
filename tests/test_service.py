# -*- coding: utf-8 -*-
import logging.config
import os
import unittest

from pysds.service import Service

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestService(unittest.TestCase):

    def setUp(self):
        logging.config.fileConfig(ROOT_DIR + "/logging_test.ini", disable_existing_loggers=False)

    def test(self):
        service = Service()
        self.assertTrue(service.success())
        self.assertFalse(service.failure())
        service.failed("some error")
        self.assertTrue(service.failure())
        self.assertFalse(service.success())
        self.assertEqual("some error", service.errormsg())
        e = Exception("some exception")
        service.catched(e)
        self.assertTrue(service.failure())
        self.assertFalse(service.success())
        self.assertEqual("Exception: some exception", service.errormsg())
