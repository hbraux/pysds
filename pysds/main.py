#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Command line"""

import sys
import os
import argparse

from pysds.app import get_app, init_app

if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    sys.stderr.write("Tool requires Python 3.6 or higher!\n")
    sys.exit(-1)
from pysds.version import __version__

DEFAULT_CFG_PATH = os.path.expanduser('~/.sds')
DEFAULT_DB_URL = 'sqlite://' + DEFAULT_CFG_PATH + "/app.db"

# Escape Codes for colors
EC_RED = '\033[31m'
EC_END = '\033[0m'

def die(*msg):
    sys.stderr.write(EC_RED)
    sys.stderr.write("Error: ")
    print(*msg, file=sys.stderr)
    sys.stderr.write(EC_END)
    sys.exit(1)


def getapp():
    app = get_app(DEFAULT_CFG_PATH)
    if not app:
        die("Application is not initialized")
    return app

def init(username, email, dburl):
    if getapp():
        die("Application is already initialized")
    init_app(DEFAULT_CFG_PATH, dburl, username, email)


def register(username, email, uuid, pubkey):
    getapp().register(username, email, uuid, pubkey)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands')

    sub1 = subparsers.add_parser("init", help="initialize the application")
    sub1.set_defaults(func=init)
    sub1.add_argument('-d', '--dburl', default=DEFAULT_DB_URL, help="Database Url")
    sub1.add_argument('username')
    sub1.add_argument('email')

    sub2 = subparsers.add_parser("register", help="register an external user")
    sub1.set_defaults(func=register)
    sub1.add_argument('username')
    sub1.add_argument('email')
    sub1.add_argument('uuid')
    sub1.add_argument('pubkey')

    parser.add_argument('--version', action='version', version="%(prog)s " + __version__)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)
    kwargs = vars(parser.parse_args())
    kwargs.pop('func')(**kwargs)


if __name__ == '__main__':
    main()
