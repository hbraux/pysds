# -*- coding: utf-8 -*-

"""Crypto class"""
# https://stuvel.eu/python-rsa-doc/usage.html#encryption-and-decryption

import hashlib
import io
import logging
import marshal
import time
from typing import BinaryIO

import rsa
from Crypto import Random
from Crypto.Cipher import AES
from rsa import PrivateKey, PublicKey

logger = logging.getLogger(__name__)


class CryptoError(Exception):
    pass


class Crypto(object):
    ENCODING = 'utf8'

    def __init__(self, pubkey: bytes = None, privkey: bytes = None, secret: bytes = None):
        self.pubkey = pubkey
        self.privkey = privkey
        self.secret = secret
        self._pub = PublicKey.load_pkcs1(pubkey, format='DER') if pubkey else None
        self._priv = PrivateKey.load_pkcs1(privkey, format='DER') if privkey else None
        self._key = self.hash(secret) if secret else None

    def genkeys(self, length: int) -> None:
        logger.info("Generating RSA keys with %d bits", length)
        (self._pub, self._priv) = rsa.newkeys(length)
        pubio = io.BytesIO()
        pubio.write(self._pub.save_pkcs1(format='DER'))
        self.pubkey = pubio.getvalue()
        privio = io.BytesIO()
        privio.write(self._priv.save_pkcs1(format='DER'))
        self.privkey = privio.getvalue()

    def hash(self, raw: bytes) -> bytes:
        m = hashlib.sha256()
        m.update(raw)
        if self.privkey:
            m.update(self.privkey)
        return m.digest()

    def asencrypt(self, raw: bytes) -> bytes:
        if not self._pub:
            raise CryptoError("Cannot encrypt without public key")
        return rsa.encrypt(raw, self._pub)

    def asdecrypt(self, raw: bytes) -> bytes:
        if not self._priv:
            raise CryptoError("Cannot decrypt without private key")
        return rsa.decrypt(raw, self._priv)

    def encrypt(self, raw: bytes) -> bytes:
        if not self._key:
            raise CryptoError("Cannot encrypt without secret")
        padding = AES.block_size - len(raw) % AES.block_size
        padded = raw + padding * bytes((padding,))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self._key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(padded)

    def decrypt(self, raw: bytes) -> bytes:
        if not self._key:
            raise CryptoError("decrypt encrypt without secret")
        iv = raw[:AES.block_size]
        cipher = AES.new(self._key, AES.MODE_CBC, iv)
        deciph = cipher.decrypt(raw[AES.block_size:])
        padding = deciph[len(deciph) - 1:][0]
        return deciph[:-padding]

    def write(self, wio: BinaryIO, line: str) -> None:
        buf = self.encrypt(line.encode(self.ENCODING))
        wio.write(len(buf).to_bytes(2, byteorder='little'))
        wio.write(buf)

    def read(self, rio: BinaryIO) -> str:
        bl = int.from_bytes(rio.read(2), byteorder='little')
        return self.decrypt(rio.read(bl)).decode(self.ENCODING)

    @staticmethod
    def lock(enckey: bytes, secret: bytes, duration: int) -> bytes:
        expir = str(int(time.time()) + duration)
        xor = str(bytes([a ^ b for a, b in zip(secret, enckey)]))
        code = eval("lambda: decrypt(bytes([a ^ b for a, b in zip(sec, " + xor + ")], raw) if time.time()<" + expir
                    + "else None")
        return marshal.dumps(code.__code__)
