#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2019 Michael Helmling, michaelhelmling@posteo.de
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
"""Setup file for pytaglib. Type <python setup.py install> to install this package."""

import io, os, sys
import re
from pathlib import Path
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

here = Path('.').parent
src = Path('src')

def readme():
    readme_file = here / 'README.md'
    return readme_file.read_text('utf-8')


is_windows = sys.platform.startswith('win')


def extension_kwargs():
    if is_windows:
        # on windows, we compile static taglib build into the python module
        taglib_install_dir = Path(os.environ.get('TAGLIB_HOME', 'build\\taglib-install'))
        taglib_lib = taglib_install_dir / 'lib' / 'tag.lib'
        if not taglib_lib.exists():
            raise FileNotFoundError(f"{taglib_lib} not found")
        return dict(
            define_macros=[('TAGLIB_STATIC', None)],
            extra_objects=[str(taglib_lib)],
            include_dirs=[str(taglib_install_dir / 'include')],
        )
    else:
        # on unix systems, use the dynamic library and rely on headers at standard location
        return dict(libraries=['tag'])


def is_cython_requested():
    return is_windows or 'PYTAGLIB_CYTHONIZE' in os.environ


if is_cython_requested():
    
    from Cython.Build import cythonize
    print('cythonizing taglib.pyx ...')
    extensions = cythonize([Extension('taglib', [str(src / 'taglib.pyx')], **extension_kwargs())], force=True)
else:
    extensions = [Extension('taglib', [str(src / 'taglib.cpp')], **extension_kwargs())]


def version():
    taglib_pyx = here / src / 'taglib.pyx'
    version_match = re.search(r"^version = ['\"]([^'\"]*)['\"]", taglib_pyx.read_text(), re.M)
    return version_match.group(1)


setup(
    name='pytaglib',
    description='cross-platform, Python audio metadata ("tagging") library based on TagLib',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=CLASSIFIERS,
    version=version(),
    license='GPLv3+',
    author='Michael Helmling',
    author_email='michaelhelmling@posteo.de',
    url='http://github.com/supermihi/pytaglib',
    ext_modules=extensions,
    package_dir={'': 'src'},
    py_modules=['pytaglib', 'pyprinttags'],
    entry_points={'console_scripts': ['pyprinttags=pyprinttags:script']},
    python_requires='>=3.6'
)
