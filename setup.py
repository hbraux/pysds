#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

from pysds.__init__ import __version__

setup(
    name='pysds',
    include_package_data=True,
    packages=find_packages(include=['pysds']),
    version=__version__,
    description="Python SYD",
    entry_points={'console_scripts': ['pysds=pysds.cli:main'], },
    install_requires=['rsa', 'sqlalchemy', 'pycryptodome'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'coverage', 'coverage-badge'],
    test_suite='tests',
    zip_safe=False
)
