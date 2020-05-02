# -*- coding: utf-8 -*-

"""Error handling"""

import logging

logger = logging.getLogger(__name__)
_last_error_msg = None


def application_error(err=None):
    global _last_error_msg
    if not err:
        return _last_error_msg
    if isinstance(err, str):
        logger.error(err)
        _last_error_msg = err
    elif isinstance(err, Exception):
        logger.error(err)
        _last_error_msg = type(err).__name__ + ': ' + getattr(err, 'message', str(err)).partition('\n')[0]
    else:
        raise Exception("unsupported parameter %s", type(err))
    return False
