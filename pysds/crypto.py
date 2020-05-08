# -*- coding: utf-8 -*-

"""Crypto class"""
# https://stuvel.eu/python-rsa-doc/usage.html#encryption-and-decryption

import hashlib
import io
import logging

import rsa
from Crypto import Random
from Crypto.Cipher import AES
from rsa import PrivateKey, PublicKey

logger = logging.getLogger(__name__)


class Crypto(object):

    def __init__(self, pubkey: bytes = None, privkey: bytes = None):
        self.pubkey = pubkey
        self.privkey = privkey
        self._pub = PublicKey.load_pkcs1(pubkey, format='DER') if pubkey else None
        self._priv = PrivateKey.load_pkcs1(privkey, format='DER') if privkey else None

    def genkeys(self, length: int) -> None:
        logger.info("Generating RSA keys with %d bits", length)
        (self._pub, self._priv) = rsa.newkeys(length)
        pubio = io.BytesIO()
        pubio.write(self._pub.save_pkcs1(format='DER'))
        self.pubkey = pubio.getvalue()
        privio = io.BytesIO()
        privio.write(self._priv.save_pkcs1(format='DER'))
        self.privkey = privio.getvalue()

    @staticmethod
    def hash(raw: bytes) -> bytes:
        m = hashlib.sha256()
        m.update(raw)
        return m.digest()

    def aencrypt(self, raw: bytes) -> bytes:
        if not self._pub:
            raise Exception("Cannot encrypt without public key")
        return rsa.encrypt(raw, self._pub)

    def adecrypt(self, raw: bytes) -> bytes:
        if not self._priv:
            raise Exception("Cannot decrypt without private key")
        return rsa.decrypt(raw, self._priv)

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





