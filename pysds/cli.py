#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Command Line Interface"""
import argparse
import json
import logging.config
import os
import sys
import uuid
from json import JSONDecodeError

from pysds.__init__ import __version__
from pysds.services import Services


if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    sys.stderr.write("Tool requires Python 3.6 or higher!\n")
    sys.exit(-1)

# Escape Codes for colors
EC_RED = '\033[31m'
EC_END = '\033[0m'
EC_GREY = '\033[37m'
LOGGING_CONF = "logging.ini"


def die(msg):
    sys.stderr.write(f"{EC_RED}{msg}{EC_END}\n")
    sys.exit(1)


def info(msg):
    print(f"{EC_GREY}{msg}{EC_END}")


def to_uuid(s: str) -> uuid.UUID:
    try:
        return uuid.UUID(s)
    except ValueError as e:
        die(f"{s} is not a UUID")


def to_json(s: str) -> dict:
    try:
        return json.loads(s)
    except (TypeError, JSONDecodeError) as e:
        die(f"{s} is not a JSON expr")


def init_app():
    if not Services.init():
        die(Services.errormsg())


def register_user(username, email, uid, pubkey):
    service = Services.user()
    if not service.add(to_uuid(uid), username, email, pubkey):
        die(service.errormsg())


def list_users():
    service = Services.user()
    for u in service.list():
        print(u)


def add_dataset(name, inputfile, outputfile, metadatafile, ignore):
    service = Services.dataset()
    meta = to_json(metadatafile.readlines() if metadatafile else '{}')
    if not service.add(name, inputfile.name, outputfile, meta, ignore=ignore):
        die(service.errormsg())


def import_dataset(datafile):
    service = Services.dataset()
    if not service.add_external(datafile):
        die(service.errormsg())


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='spcommands')

    sp1 = subparsers.add_parser("init", help="initialize the app")
    sp1.set_defaults(func=init_app)

    sp2 = subparsers.add_parser("register", help="register an external user")
    sp2.set_defaults(func=register_user)
    sp2.add_argument('username')
    sp2.add_argument('email')
    sp2.add_argument('uid')
    sp2.add_argument('pubkey')

    sp3 = subparsers.add_parser("users")
    sp3.set_defaults(func=list_users)

    sp4 = subparsers.add_parser("add", help="add an internal dataset")
    sp4.set_defaults(func=add_dataset)
    sp4.add_argument('name')
    sp4.add_argument('-o', '--outputfile', help="encoded file path")
    sp4.add_argument('-m', '--metadatafile', type=argparse.FileType('r'))
    sp4.add_argument('-i', '--ignore', action='store_true')
    sp4.add_argument('inputfile', type=argparse.FileType('rb'))

    sp5 = subparsers.add_parser("import", help="import an internal dataset")
    sp5.set_defaults(func=import_dataset)
    sp5.add_argument('datafile', type=argparse.FileType('rb'))

    parser.add_argument('--version', action='version', version="%(prog)s " + __version__)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)
    if os.path.isfile(LOGGING_CONF):
        info(f"Logging configuration set from {LOGGING_CONF}")
        logging.config.fileConfig(LOGGING_CONF, disable_existing_loggers=False)
    kwargs = vars(parser.parse_args())
    kwargs.pop('func')(**kwargs)


if __name__ == '__main__':
    main()
