#!/usr/bin/python
# -*- coding: utf-8 -*-

from dockerize import __description__, __program__, __version__
from setuptools import setup, find_packages


def read(path):
    '''Return contents of file as text.'''
    with open(path) as f:
        return f.read()


setup(
    name=__program__,
    version=__version__,
    author='Lars Kellogg-Stedman',
    author_email='lars@oddbit.com',
    description=__description__,
    long_description=read('README.rst'),
    url='https://github.com/larsks/dockerize',
    # license='GPLv3',
    keywords=['Docker'],
    packages=find_packages(),
    install_requires=read('requirements.txt').splitlines(),
    package_data={'dockerize': ['templates/*']},
    entry_points={
        'console_scripts': [
            'dockerize = dockerize.main:main'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        # 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: System',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
    ]
)
