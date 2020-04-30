import unittest
import base64

from pysds.encoder import Encoder


class EncoderTest(unittest.TestCase):
    def test_hash(self):
        encoder = Encoder()
        msg = "a sample message".encode()
        h = encoder.hash(msg)
        self.assertEqual(32, len(h))
        self.assertEqual(b'8Wc4FH/3nXdyg+Ax5KfSgRMcG8qhQ34Z3OZZOa+IXPQ=', base64.b64encode(h))


if __name__ == '__main__':
    unittest.main()
