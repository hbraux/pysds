#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

from pysds.version import __version__

setup(
    name='pysds',
    include_package_data=True,
    packages=find_packages(include=['pysds']),
    version=__version__,
    description="Python SDS",
    entry_points={'console_scripts': ['sds=pysds.cli:main'], },
    install_requires=['rsa', 'sqlalchemy', 'Crypto'],
    setup_requires=['pytest-runner', 'pycodestyle'],
    tests_require=['pytest'],
    test_suite='tests',
    zip_safe=False
)
