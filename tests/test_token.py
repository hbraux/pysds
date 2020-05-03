import unittest
import logging.config
import logging
import os
import marshal
import time

logging.config.fileConfig('logging_test.ini', disable_existing_loggers=False)

TEST_PATH = os.path.abspath(os.getcwd() + "/../target/")


class TestToken(unittest.TestCase):

    # https://stackoverflow.com/questions/16064409/how-to-create-a-code-object-in-python

    def test_generate(self):
        secret = b'secretphrase'
        inputkey = b'encryptedkey'
        exptime = str(int(time.time() + 1))
        xor = str(bytes([a ^ b for a, b in zip(secret, inputkey)]))
        l = eval("lambda: bytes([a ^ b for a, b in zip(sec, " + xor + ")]) if time.time() < " + exptime + "else None")
        bytecode = marshal.dumps(l.__code__)
        eggs = marshal.loads(bytecode)
        outputkey = eval(eggs, {'sec': secret, 'time': time})
        self.assertEqual(inputkey, outputkey)
        time.sleep(1)
        expiredkey = eval(eggs, {'sec': secret, 'time': time})
        print(expiredkey)
        self.assertNotEqual(inputkey, expiredkey)


