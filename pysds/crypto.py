# -*- coding: utf-8 -*-

"""Crypto class"""
# https://stuvel.eu/python-rsa-doc/usage.html#encryption-and-decryption

import hashlib
import rsa
import logging
import io

from Crypto import Random
from rsa import PrivateKey, PublicKey
from Crypto.Cipher import AES

logger = logging.getLogger(__name__)


class Crypto(object):

    def __init__(self, nbbits=512, pubkey: bytes = None, privkey: bytes = None, genkeys=False):
        if pubkey:
            self.pubkey = pubkey
            self.__pub = PublicKey.load_pkcs1(self.pubkey, format='DER')
            self.privkey = privkey
            if privkey:
                self.__priv = PrivateKey.load_pkcs1(self.privkey, format='DER')
            else:
                self.__priv = None
        elif genkeys:
            logger.debug("Generating RSA keys with %d bits", nbbits)
            (self.__pub, self.__priv) = rsa.newkeys(nbbits)
            pubio = io.BytesIO()
            pubio.write(self.__pub.save_pkcs1(format='DER'))
            self.pubkey = pubio.getvalue()
            privio = io.BytesIO()
            privio.write(self.__priv.save_pkcs1(format='DER'))
            self.privkey = privio.getvalue()

    @staticmethod
    def hash(raw: bytes) -> bytes:
        m = hashlib.sha256()
        m.update(raw)
        return m.digest()

    def aencrypt(self, raw: bytes) -> bytes:
        if not self.__pub:
            raise Exception("Cannot encrypt without public key")
        return rsa.encrypt(raw, self.__pub)

    def adecrypt(self, raw: bytes) -> bytes:
        if not self.__priv:
            raise Exception("Cannot decrypt without private key")
        return rsa.decrypt(raw, self.__priv)

    @staticmethod
    def encrypt(key: bytes, raw: bytes) -> bytes:
        padding = AES.block_size - len(raw) % AES.block_size
        padded = raw + padding * bytes((padding,))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(padded)

    @staticmethod
    def decrypt(key: bytes, raw: bytes) -> bytes:
        iv = raw[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        deciph = cipher.decrypt(raw[AES.block_size:])
        padding = deciph[len(deciph) - 1:][0]
        return deciph[:-padding]



