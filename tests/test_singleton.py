# -*- coding: utf-8 -*-

import unittest

from pysds.singleton import Singleton


class SampleSingleton(metaclass=Singleton):
    pass


class SampleSingletonChild(SampleSingleton):
    pass


class TestSingleton(unittest.TestCase):

    def test_singleton(self):
        singleton = SampleSingleton()
        self.assertEqual(singleton, SampleSingleton())
        SampleSingleton.destroy()
        self.assertNotEqual(singleton, SampleSingleton())

    def test_singleton_child(self):
        singleton = SampleSingletonChild()
        self.assertEqual(singleton, SampleSingletonChild())
        self.assertNotEqual(singleton, SampleSingleton())

