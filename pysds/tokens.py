# -*- coding: utf-8 -*-

"""Token Handling"""

import marshal
import time


class Tokens:

    def __init__(self):
        pass

    @staticmethod
    def create(enckey: bytes, secret: bytes, duration: int) -> bytes:
        expir = str(int(time.time()) + duration)
        xor = str(bytes([a ^ b for a, b in zip(secret, enckey)]))
        code = eval("lambda: bytes([a ^ b for a, b in zip(sec, " + xor + ")]) if time.time()<" + expir + "else None")
        return marshal.dumps(code.__code__)


