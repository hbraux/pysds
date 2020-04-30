# -*- coding: utf-8 -*-

"""Encoder class"""

import hashlib
import os
import rsa
import logging
from typing import ByteString

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

DEFAULT_CONFIG_PATH = '~/.sds'
PK_FILE = 'key.pk'
PUB_FILE = 'key.pub'
DEFAULT_RSA_BITS = 2048

class Encoder(object):
    """Encoder

    Attributes:
       tbc
    """

    def __init__(self, cfg_path=DEFAULT_CONFIG_PATH, rsa_bits=DEFAULT_RSA_BITS):
        self.cfgpath = os.path.expanduser(cfg_path)
        self.rsabits = rsa_bits
        self.__privkey = None
        self.__pubkey = None

    def loadkeys(self):
        if not os.path.isdir(self.cfgpath):
            logger.info("Creating configuration dir %s", self.cfgpath)
            os.makedirs(self.cfgpath)
        pkpath = self.cfgpath + "/" + PK_FILE
        if os.path.isfile(pkpath):
            with open(self.cfgpath + "/" + PUB_FILE, mode='rb') as filepub:
                pubdata = filepub.read()
            self.__pubkey = rsa.PublicKey.load_pkcs1(pubdata)
            with open(self.cfgpath + "/" + PK_FILE, mode='rb') as filepriv:
                privdata = filepriv.read()
            self.__privkey = rsa.PrivateKey.load_pkcs1(privdata)
            logger.info("RSA keys loaded from %s", self.cfgpath)
        else:
            logger.info("Generating RSA keys with %d bits", self.rsabits)
            (self.__pubkey, self.__privkey) = rsa.newkeys(self.rsabits)
            with open(self.cfgpath + "/" + PUB_FILE, mode='wb') as filepub:
                filepub.write(self.__pubkey.save_pkcs1())
            with open(self.cfgpath + "/" + PK_FILE, mode='wb') as filepriv:
                filepriv.write(self.__privkey.save_pkcs1())
            logger.info("RSA keys stored to %s", self.cfgpath)

    def hash(self, msg: ByteString) -> ByteString:
        m = hashlib.sha256()
        m.update(msg)
        return m.digest()

# https://stuvel.eu/python-rsa-doc/usage.html#encryption-and-decryption
    def encrypt(self, msg: ByteString) -> ByteString:
        return rsa.encrypt(msg, self.__pubkey)

    def decrypt(self, msg: ByteString) -> ByteString:
        return rsa.decrypt(msg, self.__privkey)
