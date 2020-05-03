# -*- coding: utf-8 -*-

import logging.config
import unittest

from status import Status

logging.config.fileConfig('logging_test.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class TestStatus(unittest.TestCase):

    def test_status(self):
        Status.clear()
        self.assertEqual(True, Status.success())
        self.assertEqual(False, Status.failure())
        errmsg = "this is an error"
        Status.failed(errmsg)
        self.assertEqual(True, Status.failure())
        self.assertEqual(errmsg, Status.errormsg())
        Status.clear()
        self.assertEqual(True, Status.success())
        e = Exception("Some exception")
        Status.catched(e, logger)
        self.assertEqual(True, Status.failure())
        self.assertEqual("Exception: Some exception", Status.errormsg())
