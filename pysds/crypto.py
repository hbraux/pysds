# -*- coding: utf-8 -*-

"""Crypto class"""
# https://stuvel.eu/python-rsa-doc/usage.html#encryption-and-decryption

import hashlib
import rsa
import logging
import io
import base64
from typing import ByteString
from rsa import PrivateKey, PublicKey

logger = logging.getLogger(__name__)


class Crypto(object):

    def __init__(self, nbbits=512, pubkey: ByteString = None, privkey: ByteString = None):
        if pubkey:
            self.pubkey = pubkey
            self.__pub = PublicKey.load_pkcs1(self.pubkey, format='DER')
            self.privkey = privkey
            if privkey:
                self.__priv = PrivateKey.load_pkcs1(self.privkey, format='DER')
            else:
                self.__priv = None
        else:
            logger.debug("Generating RSA keys with %d bits", nbbits)
            (self.__pub, self.__priv) = rsa.newkeys(nbbits)
            pubio = io.BytesIO()
            pubio.write(self.__pub.save_pkcs1(format='DER'))
            self.pubkey = pubio.getvalue()
            privio = io.BytesIO()
            privio.write(self.__priv.save_pkcs1(format='DER'))
            self.privkey = privio.getvalue()

    def hash(self, msg: ByteString) -> ByteString:
        m = hashlib.sha256()
        m.update(msg)
        return m.digest()

    def encrypt(self, msg: ByteString) -> ByteString:
        if not self.__pub:
            raise Exception("Cannot encrypt without public key")
        return rsa.encrypt(msg, self.__pub)

    def decrypt(self, msg: ByteString) -> ByteString:
        if not self.__priv:
            raise Exception("Cannot decrypt without private key")
        return rsa.decrypt(msg, self.__priv)
