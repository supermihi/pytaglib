#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2011-2012 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
"""Setup file for pytaglib. Type <python setup.py install> to install this package."""
 
from distutils.core import setup
from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

modules = [Extension("taglib", ["src/taglib.pyx", "src/ctypes.pxd"],
                     libraries=['tag', "stdc++"],
                     language="c++")]

setup(
  name = 'pytaglib',
  description = 'TagLib bindings for python 2.x/3.x, written using cython',
  version = '0.2.2',
  author = 'Michael Helmling',
  author_email = 'helmling@mathematik.uni-kl.de',
  url = 'http://github.com/supermihi/pytaglib',
  
  install_requires = ['cython'],
  cmdclass = {'build_ext': build_ext},
  ext_modules = modules,
  scripts = ['src/pyprinttags.py'],
  package_dir = {'': 'src'},
  test_suite = "tests",
)
