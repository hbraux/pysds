# -*- coding: utf-8 -*-

import unittest
import base64
import logging.config
import logging
from pysds.crypto import Crypto

logging.config.fileConfig('logging_test.ini', disable_existing_loggers=False)

TEST_PUBKEY =  base64.b64decode("MEgCQQChLLM582ZAE+rSsDimhXbln+8jCY5gDeyNGdgIK5crhIU3kiRJWr6V711Or2AmtMBHHoFf1rz1Mbjw+YOn4x5JAgMBAAE=")

class TestCrypto(unittest.TestCase):

    def test_hash(self):
        crypto = Crypto()
        msg = "a sample message".encode()
        h = crypto.hash(msg)
        self.assertEqual(32, len(h))
        self.assertEqual(b'8Wc4FH/3nXdyg+Ax5KfSgRMcG8qhQ34Z3OZZOa+IXPQ=', base64.b64encode(h))

    def test_encrypt_decrypt(self):
        crypto = Crypto()
        msg = 'hello Bob!'.encode()
        self.assertEqual(msg, crypto.decrypt(crypto.encrypt(msg)))

    def test_encrypt_with_pub(self):
        crypto = Crypto(pubkey=TEST_PUBKEY)
        msg = 'hello Bob!'.encode()
        self.assertEqual(64, len(crypto.encrypt(msg)))

    def test_decrypt_without_priv(self):
        crypto = Crypto(pubkey=TEST_PUBKEY)
        msg = 'hello Bob!'.encode()
        self.assertRaises(Exception, crypto.decrypt, msg)


if __name__ == '__main__':
    unittest.main()
