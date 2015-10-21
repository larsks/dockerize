#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from dockerize import __version__

with open('requirements.txt') as fd:
    setup(name='dockerize',
          version=__version__,
          packages=find_packages(),
          install_requires=fd.readlines(),
          package_data={'dockerize': ['templates/*']},
          entry_points={
              'console_scripts': [
                  'dockerize = dockerize.main:main',
              ],
          }
          )
