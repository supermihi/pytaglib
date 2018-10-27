#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2018 Michael Helmling, michaelhelmling@posteo.de
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
"""Setup file for pytaglib. Type <python setup.py install> to install this package."""

import io, os, os.path, sys
import re
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
    readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
    if sys.version_info[0] >= 3:
        return open(readme_file, 'rt', encoding='utf-8').read()
    else:
        return open(readme_file, 'rt').read()


script_name = 'pyprinttags3' if sys.version_info[0] >= 3 else 'pyprinttags'
is_windows = sys.platform.startswith('win')

if is_windows:
    # on windows, we compile static taglib build into the python module
    TAGLIB_HOME = os.environ.get('TAGLIB_HOME', 'C:\\Libraries\\taglib')
    kwargs = dict(
        define_macros=[('TAGLIB_STATIC', None)],
        extra_objects=[os.path.join(TAGLIB_HOME, 'lib', 'tag.lib')],
        include_dirs=[os.path.join(TAGLIB_HOME, 'include')],
    )
else:
    # on unix systems, use the dynamic library and rely on headers at standard location
    kwargs = dict(libraries=['tag'])

if '--cython' in sys.argv or is_windows:
    from Cython.Build import cythonize
    print('cythonizing taglib.pyx ...')
    extensions = cythonize([Extension('taglib', [os.path.join('src', 'taglib.pyx')], **kwargs)])
    sys.argv = [arg for arg in sys.argv if arg != '--cython']
else:
    extensions = [Extension('taglib', [os.path.join('src', 'taglib.cpp')], **kwargs)]


def version():
    with io.open(os.path.join('src', 'taglib.pyx'), 'rt', encoding='UTF-8') as pyx:
        version_match = re.search(r"^version = ['\"]([^'\"]*)['\"]", pyx.read(), re.M)
        return version_match.group(1)


setup(
    name='pytaglib',
    description='cross-platform, Python 2.x/3.x audio metadata ("tagging") library based on TagLib',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=CLASSIFIERS,
    version=version(),
    license='GPLv3+',
    author='Michael Helmling',
    author_email='michaelhelmling@posteo.de',
    url='http://github.com/supermihi/pytaglib',
    ext_modules=extensions,
    package_dir={'': 'src', 'tests': ''},
    py_modules=['pyprinttags'],
    entry_points={'console_scripts': ['{0} = pyprinttags:script'.format(script_name)]},
    test_suite='tests',
)
