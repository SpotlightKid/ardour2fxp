#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# setup.py
#
"""Setup file for ardour2fxp."""

from io import open
from os.path import join
from setuptools import setup


def read(*paths):
    with open(join(*paths), encoding='utf-8') as fp:
        return fp.read()


classifiers = """
Development Status :: 4 - Beta
Environment :: Console
Intended Audience :: End Users/Desktop
License :: OSI Approved :: MIT License
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX :: Linux
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3 :: Only
Topic :: Multimedia :: Sound/Audio
Topic :: Utilities
"""

setup(
    name='ardour2fxp',
    version="0.1.0b1",
    description=read('README.rst').splitlines()[3],
    long_description="\n".join(read('README.rst').splitlines()[3:]),
    author="Christopher Arndt",
    author_email="info@chrisarndt.de",
    url="https://github.com/SpotlightKid/ardour2fxp",
    py_modules=["ardour2fxp", "fxp2ardour"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "ardour2fxp = ardour2fxp:main",
            "fxp2ardour = fxp2ardour:main"
        ]
    },
    classifiers=[c.strip() for c in classifiers.splitlines()
                 if c.strip() and not c.startswith('#')]
)
