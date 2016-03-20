# -*- coding: utf-8 -*-
# Copyright 2011-2016 Michael Helmling, michaelhelmling@posteo.de
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation

"""This file contains the relevant MPEG headers needed for the ID3v2 workaround in taglib versions
before release 1.9.0.
"""
 
cimport ctypes

cdef extern from 'taglib/mpegfile.h' namespace 'TagLib::MPEG':
    cdef cppclass File(ctypes.File):
        bint save(bint, int)
