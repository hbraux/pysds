# -*- coding: utf-8 -*-

"""Data Model"""
import logging

from pysds.singleton import Singleton

logger = logging.getLogger(__name__)


class Service(metaclass=Singleton):
    """This is the parent class of all Services. Handle status and error messages and provide singleton pattern"""
    _error_msg = None

    @classmethod
    def failed(cls, msg) -> None:
        logger.error(msg)
        cls._error_msg = msg
        return None

    @classmethod
    def catched(cls, e: Exception) -> None:
        msg = type(e).__name__ + ': ' + getattr(e, 'message', str(e)).partition('\n')[0]
        return cls.failed(msg)

    @classmethod
    def failure(cls) -> bool:
        return cls._error_msg is not None

    @classmethod
    def success(cls) -> bool:
        return cls._error_msg is None

    @classmethod
    def errormsg(cls) -> str:
        return cls._error_msg

