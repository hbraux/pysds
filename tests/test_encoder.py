import unittest
import base64
import os
import shutil
from pysds.encoder import Encoder

TEST_CONFIG_DIR = os.getcwd() + "/../target/"
TEST_RSA_BITS = 512

class EncoderTest(unittest.TestCase):

    def test_hash(self):
        encoder = Encoder(cfg_path=TEST_CONFIG_DIR, rsa_bits=TEST_RSA_BITS)
        msg = "a sample message".encode()
        h = encoder.hash(msg)
        self.assertEqual(32, len(h))
        self.assertEqual(b'8Wc4FH/3nXdyg+Ax5KfSgRMcG8qhQ34Z3OZZOa+IXPQ=', base64.b64encode(h))

    def test_loadkeys(self):
        if os.path.isdir(TEST_CONFIG_DIR):
            shutil.rmtree(TEST_CONFIG_DIR)
        encoder = Encoder(cfg_path=TEST_CONFIG_DIR, rsa_bits=TEST_RSA_BITS)
        encoder.loadkeys()
        self.assertTrue(os.path.isfile(TEST_CONFIG_DIR + "key.pk"), "private key file exists")
        self.assertTrue(os.path.isfile(TEST_CONFIG_DIR + "key.pub"), "public key file exists")

    def test_encrypt(self):
        encoder = Encoder(cfg_path=TEST_CONFIG_DIR, rsa_bits=TEST_RSA_BITS)
        encoder.loadkeys()
        msg = 'hello Bob!'.encode('utf8')
        self.assertEqual(msg, encoder.decrypt(encoder.encrypt(msg)))


if __name__ == '__main__':
    unittest.main()
