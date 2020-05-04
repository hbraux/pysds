# -*- coding: utf-8 -*-

"""Error handling"""


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
    def failed(msg: str):
        _status._errmsg = msg

    @staticmethod
    def catched(e: Exception):
        msg = type(e).__name__ + ': ' + getattr(e, 'message', str(e)).partition('\n')[0]
        _status._errmsg = msg


_status = Status()
