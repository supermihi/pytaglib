# -*- coding: utf-8 -*-
# Copyright 2012 Michael Helmling, michaelhelmling@posteo.de
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation

"""This file contains the relevant MPEG headers needed for the ID3v2 workaround."""
 
cimport ctypes

cdef extern from "taglib/id3v2tag.h" namespace "TagLib::ID3v2":
    cdef cppclass Tag

cdef extern from "taglib/mpegfile.h" namespace "TagLib::MPEG":
    cdef cppclass File(ctypes.File):
        Tag* ID3v2Tag(bint)
        bint strip(int)
        bint save(bint, int)
