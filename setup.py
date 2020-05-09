#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

from pysyd.__init__ import __version__

setup(
    name='pysyd',
    include_package_data=True,
    packages=find_packages(include=['pysyd']),
    version=__version__,
    description="Python SYD",
    entry_points={'console_scripts': ['syd=pysyd.cli:main'], },
    install_requires=['rsa', 'sqlalchemy', 'crypto', 'injector'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    zip_safe=False
)
