#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Command Line Interface"""
import os
import sys
import argparse
import logging.config

from pysds.services import Services
from pysds.__init__ import __version__

if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    sys.stderr.write("Tool requires Python 3.6 or higher!\n")
    sys.exit(-1)


# Escape Codes for colors
EC_RED = '\033[31m'
EC_END = '\033[0m'
LOGGING_CONF = "logging.ini"


def die(*msg):
    sys.stderr.write(EC_RED)
    print(*msg, file=sys.stderr)
    sys.stderr.write(EC_END)
    sys.exit(1)


def init_app():
    if not Services.init():
        die(Services.errormsg())


def register_user(username, email, uuid, pubkey):
    service = Services.user()
    if not service.add(username, email, uuid, pubkey):
        die(service.errormsg())


def list_users():
    service = Services.user()
    for u in service.list():
        print(u)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands')

    sub1 = subparsers.add_parser("init", help="initialize the app")
    sub1.set_defaults(func=init_app)

    sub2 = subparsers.add_parser("register", help="register an external user")
    sub2.set_defaults(func=register_user)
    sub2.add_argument('username')
    sub2.add_argument('email')
    sub2.add_argument('uuid')
    sub2.add_argument('pubkey')

    sub3 = subparsers.add_parser("users")
    sub3.set_defaults(func=list_users)

    parser.add_argument('--version', action='version', version="%(prog)s " + __version__)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)
    if os.path.isfile(LOGGING_CONF):
        print("Loading Logging configuration from", LOGGING_CONF)
        logging.config.fileConfig(LOGGING_CONF, disable_existing_loggers=False)
    kwargs = vars(parser.parse_args())
    kwargs.pop('func')(**kwargs)


if __name__ == '__main__':
    main()
