# -*- coding: utf-8 -*-

"""Error handling"""

from singleton import Singleton


class AppError(metaclass=Singleton):

    def __init__(self, msg=None):
        self._msg = msg
        pass

    @staticmethod
    def found() -> bool:
        return AppError()._msg is not None

    @staticmethod
    def msg() -> str:
        return AppError()._msg

    @staticmethod
    def catched(e: Exception) -> None:
        AppError(type(e).__name__ + ': ' + getattr(e, 'message', str(e)).partition('\n')[0])
