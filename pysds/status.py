# -*- coding: utf-8 -*-

"""Error handling"""
from logging import Logger


class Status:

    def __init__(self):
        self._errmsg = None

    @staticmethod
    def failure() -> bool:
        return _status._errmsg is not None

    @staticmethod
    def success() -> bool:
        return _status._errmsg is None

    @staticmethod
    def clear() -> None:
        _status._errmsg = None

    @staticmethod
    def errormsg() -> str:
        return _status._errmsg

    @staticmethod
    def failed(msg: str, logger: Logger = None) -> None:
        if logger:
            logger.error(msg)
        _status._errmsg = msg
        return None

    @staticmethod
    def catched(e: Exception, logger: Logger = None) -> None:
        msg = type(e).__name__ + ': ' + getattr(e, 'message', str(e)).partition('\n')[0]
        if logger:
            logger.error(msg)
        _status._errmsg = msg
        return None


_status = Status()
