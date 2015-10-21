#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from dockerize import __version__


def read(path):
    with open(path) as fd:
        return fd.read().splitlines()

setup(
    name='dockerize',
    version=__version__,
    packages=find_packages(),
    install_requires=read('requirements.txt'),
    package_data={'dockerize': ['templates/*']},
    entry_points={
        'console_scripts': [
            'dockerize = dockerize.main:main'
        ]
    }
)
