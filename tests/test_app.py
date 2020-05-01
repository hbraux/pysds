# -*- coding: utf-8 -*-

import unittest
import os
import shutil

from pysds.app import App

TEST_PATH = os.path.abspath(os.getcwd() + "/../target/")
TEST_URL = 'sqlite:///:memory:'

class TestApp(unittest.TestCase):
    def test_init(self):
        cleanup()
        App.init(TEST_PATH, TEST_URL, 512, "testuser", "email@cie.org")



def cleanup():
    if os.path.isdir(TEST_PATH):
        shutil.rmtree(TEST_PATH)


