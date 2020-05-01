#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Command Line Interface"""

import sys
import os
import argparse
import logging.config

if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    sys.stderr.write("Tool requires Python 3.6 or higher!\n")
    sys.exit(-1)

from pysds.app import App
from pysds.version import __version__

DEFAULT_CFG_PATH = os.path.expanduser('~/.sds')
DEFAULT_DB_URL = 'sqlite://' + DEFAULT_CFG_PATH + "/app.db"
DEFAULT_RSA_BITS = 2048

# Escape Codes for colors
EC_RED = '\033[31m'
EC_END = '\033[0m'

logging.config.fileConfig('logging.ini')

def die(*msg):
    sys.stderr.write(EC_RED)
    sys.stderr.write("Error: ")
    print(*msg, file=sys.stderr)
    sys.stderr.write(EC_END)
    sys.exit(1)

def getapp():
    app = App.get_instance(DEFAULT_CFG_PATH)
    if not app:
        die("Application is not initialized")
    return app


def init(username, email, dburl, bits):
    if App.get_instance(DEFAULT_CFG_PATH):
        die("Application is already initialized")
    App.init(DEFAULT_CFG_PATH, dburl, bits, username, email)


def register_user(username, email, uuid, pubkey):
    getapp().register(username, email, uuid, pubkey)

def list_users():
    pass

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands')

    sub1 = subparsers.add_parser("init", help="initialize the application")
    sub1.set_defaults(func=init)
    sub1.add_argument('-d', '--dburl', default=DEFAULT_DB_URL, help="Database Url")
    sub1.add_argument('-b', '--bits', default=DEFAULT_RSA_BITS, help="RSA key length in bits")
    sub1.add_argument('username')
    sub1.add_argument('email')

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
