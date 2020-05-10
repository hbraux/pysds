# -*- coding: utf-8 -*-
import base64
import logging.config
import os
import unittest
import uuid

from pysds.crypto import Crypto, CryptoError

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

    def test_asym_encrypt_adecrypt(self):
        crypto = Crypto()
        crypto.genkeys(512)
        msg = 'hello Bob!'.encode()
        self.assertEqual(msg, crypto.asdecrypt(crypto.asencrypt(msg)))

    def test_asym_encrypt_with_pub(self):
        crypto = Crypto(pubkey=TEST_PUBKEY)
        msg = 'hello Bob!'.encode()
        self.assertEqual(64, len(crypto.asencrypt(msg)))

    def test_asym_decrypt_without_priv(self):
        crypto = Crypto(pubkey=TEST_PUBKEY)
        msg = 'hello Bob!'.encode()
        self.assertRaises(CryptoError, crypto.asdecrypt, msg)

    def test_encrypt_decrypt(self):
        crypto = Crypto(secret=uuid.uuid4().bytes)
        msg = 'hello Bob!'.encode()
        self.assertEqual(msg, crypto.decrypt(crypto.encrypt(msg)))

    def test_encrypt_decrypt16(self):
        crypto = Crypto(secret=uuid.uuid4().bytes)
        msg = '1234567890ABCDEF'.encode()
        self.assertEqual(msg, crypto.decrypt(crypto.encrypt(msg)))

    def test_encrypt_without_secret(self):
        crypto = Crypto()
        msg = 'hello Bob!'.encode()
        self.assertRaises(CryptoError, crypto.encrypt, msg)

    def test_write_read(self):
        crypto = Crypto(secret=uuid.uuid4().bytes)
        line = 'some line to encrypt'
        tstfile = ROOT_DIR + "/crypto.sds"
        with open(tstfile, "wb") as wio:
            crypto.write(wio, line)
        with open(tstfile, "rb") as rio:
            rline = crypto.read(rio)
        self.assertEqual(line, rline)



