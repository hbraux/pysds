# -*- coding: utf-8 -*-

"""Crypto class"""
# https://stuvel.eu/python-rsa-doc/usage.html#encryption-and-decryption

import hashlib
import rsa
import logging
from typing import ByteString

logger = logging.getLogger(__name__)

DEFAULT_RSA_BITS = 2048

class Crypto(object):

    def __init__(self, bits: int = DEFAULT_RSA_BITS, pubkey: str = None, privkey: str = None, genkeys: str = False):
        if genkeys:
            logger.debug("Generating RSA keys")
            (self.pubkey, self.privkey) = rsa.newkeys(bits)
        else:
            self.privkey = privkey
            self.pubkey = pubkey

    def hash(self, msg: ByteString) -> ByteString:
        m = hashlib.sha256()
        m.update(msg)
        return m.digest()


    def encrypt(self, msg: ByteString) -> ByteString:
        return rsa.encrypt(msg, self.pubkey)

    def decrypt(self, msg: ByteString) -> ByteString:
        return rsa.decrypt(msg, self.privkey)
