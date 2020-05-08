# -*- coding: utf-8 -*-
import logging.config
import os
import unittest
import base64

from pysds.crypto import Crypto

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_PUBKEY = base64.b64decode(
    "MEgCQQChLLM582ZAE+rSsDimhXbln+8jCY5gDeyNGdgIK5crhIU3kiRJWr6V711Or2AmtMBHHoFf1rz1Mbjw+YOn4x5JAgMBAAE=")


class TestCrypto(unittest.TestCase):

    def setUp(self) -> None:
        logging.config.fileConfig(ROOT_DIR + "/logging_test.ini", disable_existing_loggers=False)

    def test_hash(self):
        crypto = Crypto()
        msg = "a sample message".encode()
        h = crypto.hash(msg)
        self.assertEqual(32, len(h))
        self.assertEqual(b'8Wc4FH/3nXdyg+Ax5KfSgRMcG8qhQ34Z3OZZOa+IXPQ=', base64.b64encode(h))

    def test_genkeys(self):
        crypto = Crypto()
        crypto.genkeys(256)
        self.assertIsNotNone(crypto.pubkey)
        self.assertIsNotNone(crypto.privkey)
        self.assertEqual(42, len(crypto.pubkey))

    def test_aencrypt_adecrypt(self):
        crypto = Crypto()
        crypto.genkeys(512)
        msg = 'hello Bob!'.encode()
        self.assertEqual(msg, crypto.adecrypt(crypto.aencrypt(msg)))

    def test_aencrypt_with_pub(self):
        crypto = Crypto(pubkey=TEST_PUBKEY)
        msg = 'hello Bob!'.encode()
        self.assertEqual(64, len(crypto.aencrypt(msg)))

    def test_adecrypt_without_priv(self):
        crypto = Crypto(pubkey=TEST_PUBKEY)
        msg = 'hello Bob!'.encode()
        self.assertRaises(Exception, crypto.adecrypt, msg)

    def test_encrypt_decrypt(self):
        crypto = Crypto()
        msg = 'hello Bob!'.encode()
        key = crypto.hash("secret".encode())
        self.assertEqual(msg, crypto.decrypt(key, crypto.encrypt(key, msg)))

    def test_encrypt_decrypt16(self):
        crypto = Crypto()
        msg = '1234567890ABCDEF'.encode()
        key = crypto.hash("secret".encode())
        self.assertEqual(msg, crypto.decrypt(key, crypto.encrypt(key, msg)))

