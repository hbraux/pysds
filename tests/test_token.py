import unittest
import logging.config
import logging
import os
import marshal
logging.config.fileConfig('logging_test.ini', disable_existing_loggers=False)

TEST_PATH = os.path.abspath(os.getcwd() + "/../target/")

class TestToken(unittest.TestCase):

# https://stackoverflow.com/questions/16064409/how-to-create-a-code-object-in-python

    def test_generate(self):
        secret = b'secretphrase'
        key    = b'encryptedkey'
        x =  bytes([ a ^ b for a,b in zip(secret, key) ])
        fcode = None
        exec("def f():\treturn x + 1\nfcode = f.__code__\n")
        bytecode = marshal.dumps(fcode)
        eggs = marshal.loads(bytecode)
        y = eval(eggs, {'x':1})





