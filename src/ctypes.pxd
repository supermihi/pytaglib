# -*- coding: utf-8 -*-
# Copyright 2011-2012 Michael Helmling, michaelhelmling@posteo.de
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation

"""This file contains the external C/C++ definitions used by taglib.pyx."""

from libcpp.list cimport list
from libcpp.utility cimport pair
from libcpp.string cimport string
from libcpp.map cimport map

cdef extern from *:
    ctypedef char const_char "const char"
	

cdef extern from "taglib/tstring.h" namespace "TagLib::String":
    cdef enum Type:
        # this is a bit ugly since it relies on the order in TagLib never being
        # changed, but it seems to be the only way
        Latin1, UTF16, UTF16BE, UTF8, UTF16LE


cdef extern from "taglib/tstring.h" namespace "TagLib":
    cdef cppclass String:
        String(char*, Type)
        String()
        string to8Bit(bool)
        const_char* toCString(bool)


cdef extern from "taglib/tstringlist.h" namespace "TagLib":
    cdef cppclass StringList:
        list[String].iterator begin()
        list[String].iterator end()
        void append(String&)


cdef extern from "taglib/tpropertymap.h" namespace "TagLib":
    cdef cppclass PropertyMap:
        map[String,StringList].iterator begin()
        map[String,StringList].iterator end()
        StringList& operator[](String&)
        StringList& unsupportedData()
        int size()
        void clear()

    
cdef extern from "taglib/audioproperties.h" namespace "TagLib":
    cdef cppclass AudioProperties:
        int length()
        int bitrate()
        int sampleRate()
        int channels()


cdef extern from "taglib/tfile.h" namespace "TagLib":
    cdef cppclass File:
        AudioProperties *audioProperties()
        bint save() except +
        bint isValid()
        bint readOnly()
        PropertyMap properties()
        PropertyMap setProperties(PropertyMap&)
        void removeUnsupportedProperties(StringList&)

cdef extern from "taglib/fileref.h" namespace "TagLib::FileRef":
    cdef File* create(char* fn) except +
    

ctypedef map[String,StringList].iterator mapiter
ctypedef list[String].iterator listiter # no idea why StringList.Iterator does not work here
