#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2011 Michael Helmlnig
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("taglib", ["src/taglib.pyx", "src/ctypes.pxd"],
                         libraries=['tag', "stdc++"],
                         language="c++",
                         extra_compile_args=["-fpermissive"])]

setup(
  name = 'pyTagLib',
  author = 'Michael Helmling',
  author_email = 'supermihi@web.de',
  url = 'http://github.com/supermihi/pytaglib',
  description = 'TagLib bindings for python, using Cython',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules,
  scripts = ['src/pyprinttags.py'],
  version = '0.1',
  
)
