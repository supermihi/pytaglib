#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2011-2012 Michael Helmling, michaelhelmling@posteo.de
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
"""Setup file for pytaglib. Type <python setup.py install> to install this package."""
 
import os.path, sys
from setuptools import setup
from Cython.Build import cythonize

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Cython',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


def readme():
    readmeFile = os.path.join(os.path.dirname(__file__), 'README.rst')
    if sys.version_info.major >= 3:
        return open(readmeFile, "rt", encoding='utf-8').read()
    else:
        return open(readmeFile, "rt").read()

script_name = 'pyprinttags3' if sys.version_info.major >= 3 else 'pyprinttags'

setup(
    name='pytaglib',
    description='Python (2.7+/3.1+) bindings for the TagLib audio metadata library',
    long_description=readme(),
    classifiers=CLASSIFIERS,
    version='0.3.3',
    license='GPLv3+',
    author='Michael Helmling',
    author_email='michaelhelmling@posteo.de',
    url='http://github.com/supermihi/pytaglib',
    install_requires=['cython>=0.16'],
    ext_modules=cythonize("src/taglib.pyx"),
    package_dir={'': 'src'},
    py_modules=['pyprinttags'],
    entry_points={ 'console_scripts': ['{} = pyprinttags:script'.format(script_name)] },
    test_suite='tests'
)
