# -*- coding: utf-8 -*-
# Copyright 2011-2024 Michael Helmling, michaelhelmling@posteo.de
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation

"""This file contains the external C/C++ definitions used by taglib.pyx."""

from libc.stddef cimport wchar_t
from libcpp.list cimport list
from libcpp.map cimport map
from libcpp.string cimport string
from cpython.mem cimport PyMem_Free
from cpython.object cimport PyObject


cdef extern from "Python.h":
    cdef wchar_t *PyUnicode_AsWideCharString(PyObject *path, Py_ssize_t *size)


cdef extern from 'taglib/tstring.h' namespace 'TagLib::String':
    cdef extern enum Type:
        Latin1, UTF16, UTF16BE, UTF8, UTF16LE


cdef extern from 'taglib/tstring.h' namespace 'TagLib':
    cdef cppclass String:
        String()
        String(char*, Type)
        string to8Bit(bint)


cdef extern from 'taglib/tstringlist.h' namespace 'TagLib':
    cdef cppclass StringList:
        list[String].iterator begin()
        list[String].iterator end()
        void append(String&)


cdef extern from 'taglib/tpropertymap.h' namespace 'TagLib':
    cdef cppclass PropertyMap:
        map[String,StringList].iterator begin()
        map[String,StringList].iterator end()
        StringList& operator[](String&)
        StringList& unsupportedData()
        int size()


cdef extern from 'taglib/audioproperties.h' namespace 'TagLib':
    cdef cppclass AudioProperties:
        int lengthInMilliseconds()
        int bitrate()
        int sampleRate()
        int channels()

cdef extern from 'taglib/audioproperties.h' namespace 'TagLib::AudioProperties':
    cdef enum ReadStyle:
        Fast = 0
        Average = 1
        Accurate = 2

cdef extern from 'taglib/tfile.h' namespace 'TagLib':
    cdef cppclass File:
        AudioProperties *audioProperties()
        bint save() except +
        bint isValid()
        bint readOnly()
        PropertyMap properties()
        PropertyMap setProperties(PropertyMap&)
        void removeUnsupportedProperties(StringList&)


cdef extern from 'taglib/tiostream.h' namespace 'TagLib':
    IF UNAME_SYSNAME != "Windows":
        ctypedef char* FileName
    ELSE:
        cdef cppclass FileName:
            FileName(const wchar_t*)

cdef extern from 'taglib/fileref.h' namespace 'TagLib':
    cdef cppclass FileRef:
        FileRef(FileName, boolean, ReadStyle) except +
        File* file()

        AudioProperties *audioProperties()
        bint save() except +
        PropertyMap properties()
        PropertyMap setProperties(PropertyMap&)
        void removeUnsupportedProperties(StringList&)

cdef inline FileRef* create_wrapper(unicode path) except +:
    IF UNAME_SYSNAME != "Windows":
        return new FileRef(path.encode('utf-8'), True, ReadStyle.Average)
    ELSE:
        cdef wchar_t *wchar_path = PyUnicode_AsWideCharString(<PyObject*>path, NULL)
        cdef FileRef *file_ref = new FileRef(FileName(wchar_path), True, ReadStyle.Average)
        PyMem_Free(wchar_path)
        return file_ref

cdef extern from 'taglib/taglib.h':
    int TAGLIB_MAJOR_VERSION
    int TAGLIB_MINOR_VERSION
