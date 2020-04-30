# -*- coding: utf-8 -*-

"""Encoder class"""

import sys
import uuid
import time
import hashlib
from typing import ByteString


class Encoder(object):
    """Encoder

    Attributes:
       tbc
    """

    def __init__(self):
        return

    def hash(self, msg: ByteString) -> ByteString:
        m = hashlib.sha256()
        m.update(msg)
        return m.digest()


