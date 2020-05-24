# -*- coding: utf-8 -*-
import logging.config
import os
import unittest

from pysds.singleton import Singleton

logger = logging.getLogger(__name__)


class Asingleton(metaclass=Singleton):
    def __init__(self):
        self.some_prop = 1


class Bsingleton(metaclass=Singleton):
    def __init__(self, a_class=Asingleton):
        self.a = a_class()

    def some_method(self):
        return self.a.some_prop


class TestSingleton(unittest.TestCase):

    @classmethod
    def setUp(cls):
        logging.config.fileConfig(os.path.dirname(__file__) + "/logging_test.ini", disable_existing_loggers=False)

    def test_singleton(self):
        singleton = Asingleton()
        self.assertEqual(singleton, Asingleton())
        self.assertEqual(1, singleton.some_prop)
        Asingleton.destroy()
        self.assertNotEqual(singleton, Asingleton())

    def test_singleton_dependency(self):
        singleton = Bsingleton()
        self.assertEqual(singleton.a, Asingleton())
        self.assertTrue(singleton.some_method())

    def test_wrong_singleton(self):
        with self.assertRaises(Exception) as error:
            exec("""
class WrongSingleton(metaclass=Singleton):
    def __init__(self, someatt):
        pass
""")
        self.assertEqual('<Singleton(WrongSingleton)> does not have a valid init method', str(error.exception))


