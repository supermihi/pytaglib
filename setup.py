#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2011-2016 Michael Helmling, michaelhelmling@posteo.de
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
"""Setup file for pytaglib. Type <python setup.py install> to install this package."""

import os, os.path, sys
from setuptools import setup
from distutils.extension import Extension

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
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
    readmeFile = os.path.join(os.path.dirname(__file__), 'README.txt')
    if sys.version_info[0] >= 3:
        return open(readmeFile, 'rt', encoding='utf-8').read()
    else:
        return open(readmeFile, 'rt').read()


scriptName = 'pyprinttags3' if sys.version_info[0] >= 3 else 'pyprinttags'

if sys.platform.startswith('win'):
    # on windows, we compile static taglib build into the python module
    TAGLIB_HOME = os.environ.get('TAGLIB_HOME', 'C:\\Libraries\\taglib')
    kwargs = dict(
        define_macros=[('TAGLIB_STATIC', None)],
        extra_objects=[os.path.join(TAGLIB_HOME, 'lib', 'tag.lib')],
        include_dirs=[os.path.join(TAGLIB_HOME, 'include')],
    )
else:
    # on unix system,s use the dynamic library and rely on headers at standard location
    kwargs = dict(libraries=['tag'])

if '--cython' in sys.argv:
    from Cython.Build import cythonize

    extensions = cythonize([Extension('taglib', [os.path.join('src', 'taglib.pyx')], **kwargs)])
    sys.argv.remove('--cython')
else:
    extensions = [Extension('taglib', [os.path.join('src', 'taglib.cpp')], **kwargs)]

setup(
    name='pytaglib',
    description='Python (2.6+/3.1+) bindings for the TagLib audio metadata library',
    long_description=readme(),
    classifiers=CLASSIFIERS,
    version='1.2.1',
    license='GPLv3+',
    author='Michael Helmling',
    author_email='michaelhelmling@posteo.de',
    url='http://github.com/supermihi/pytaglib',
    ext_modules=extensions,
    package_dir={'': 'src'},
    py_modules=['pyprinttags'],
    entry_points={'console_scripts': ['{0} = pyprinttags:script'.format(scriptName)]},
    test_suite='tests'
)
