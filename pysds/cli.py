#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Command Line Interface"""

import sys
import argparse
import logging.config
from status import Status
from services import UserService

if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    sys.stderr.write("Tool requires Python 3.6 or higher!\n")
    sys.exit(-1)

from __init__ import __version__

logging.config.fileConfig('logging_test.ini', disable_existing_loggers=True)


# Escape Codes for colors
EC_RED = '\033[31m'
EC_END = '\033[0m'


def die(*msg):
    sys.stderr.write(EC_RED)
    sys.stderr.write("Error: ")
    print(*msg, file=sys.stderr)
    sys.stderr.write(EC_END)
    sys.exit(1)


def register_user(username, email, uuid, pubkey):
    if not UserService().add(username, email, uuid, pubkey):
        die(Status.errormsg())


def list_users():
    for u in UserService().list():
        print(u)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands')

    sub2 = subparsers.add_parser("register", help="register an external user")
    sub2.set_defaults(func=register_user)
    sub2.add_argument('username')
    sub2.add_argument('email')
    sub2.add_argument('uuid')
    sub2.add_argument('pubkey')

    sub3 = subparsers.add_parser("list_users")
    sub3.set_defaults(func=list_users)

    parser.add_argument('--version', action='version', version="%(prog)s " + __version__)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)
    kwargs = vars(parser.parse_args())
    kwargs.pop('func')(**kwargs)


if __name__ == '__main__':
    main()
