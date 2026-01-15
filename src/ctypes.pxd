# -*- coding: utf-8 -*-
# Copyright 2011-2024 Michael Helmling, michaelhelmling@posteo.de
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation

"""This file contains the external C/C++ definitions used by taglib.pyx."""

from libcpp cimport bool as cppbool
from libcpp.list cimport list
from libcpp.map cimport map
from libcpp.string cimport string


cdef extern from 'taglib/tstring.h' namespace 'TagLib::String':
    cdef extern enum Type:
        Latin1, UTF16, UTF16BE, UTF8, UTF16LE


cdef extern from 'taglib/tstring.h' namespace 'TagLib':
    cdef cppclass String:
        String()
        String(char*, Type)
        string to8Bit(bint)


cdef extern from 'taglib/tbytevector.h' namespace 'TagLib':
    cdef cppclass ByteVector:
        ByteVector()
        ByteVector(const char* data, unsigned int length)
        const char* data()
        unsigned int size()
        cppbool isEmpty()


cdef extern from 'taglib/tstringlist.h' namespace 'TagLib':
    cdef cppclass StringList:
        list[String].iterator begin()
        list[String].iterator end()
        void append(String&)


cdef extern from 'taglib/tmap.h' namespace 'TagLib':
    cdef cppclass Map[K, V]:
        Map()
        map[K, V].iterator begin()
        map[K, V].iterator end()
        V& operator[](const K&)
        unsigned int size()
        cppbool isEmpty()


cdef extern from 'taglib/tlist.h' namespace 'TagLib':
    cdef cppclass List[T]:
        List()
        list[T].iterator begin()
        list[T].iterator end()
        void append(const T&)
        unsigned int size()
        cppbool isEmpty()


cdef extern from 'taglib/tvariant.h' namespace 'TagLib::Variant':
    cdef extern enum VariantType "TagLib::Variant::Type":
        Void "TagLib::Variant::Void"
        Bool "TagLib::Variant::Bool"
        Int "TagLib::Variant::Int"
        UInt "TagLib::Variant::UInt"
        LongLong "TagLib::Variant::LongLong"
        ULongLong "TagLib::Variant::ULongLong"
        Double "TagLib::Variant::Double"
        VString "TagLib::Variant::String"
        VStringList "TagLib::Variant::StringList"
        VByteVector "TagLib::Variant::ByteVector"
        VByteVectorList "TagLib::Variant::ByteVectorList"
        VVariantList "TagLib::Variant::VariantList"
        VVariantMap "TagLib::Variant::VariantMap"


cdef extern from 'taglib/tvariant.h' namespace 'TagLib':
    cdef cppclass Variant:
        Variant()
        Variant(int val)
        Variant(const String& val)
        Variant(const ByteVector& val)
        Variant(const Map[String, Variant]& val)
        VariantType type()
        cppbool isEmpty()
        int toInt(cppbool* ok)
        unsigned int toUInt(cppbool* ok)
        cppbool toBool(cppbool* ok)
        String toString(cppbool* ok)
        ByteVector toByteVector(cppbool* ok)
        Map[String, Variant] toMap(cppbool* ok)

# Convenience typedef for use in Python code
ctypedef Map[String, Variant] VariantMap


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

cdef extern from 'taglib/fileref.h' namespace 'TagLib':
    cdef cppclass FileRef:
        File* file()

        AudioProperties *audioProperties()
        bint save() except +
        PropertyMap properties()
        PropertyMap setProperties(PropertyMap&)
        void removeUnsupportedProperties(StringList&)
        StringList complexPropertyKeys()
        List[VariantMap] complexProperties(const String& key)
        cppbool setComplexProperties(const String& key, const List[VariantMap]& value)

cdef extern from 'taglib/taglib.h':
    int TAGLIB_MAJOR_VERSION
    int TAGLIB_MINOR_VERSION

cdef extern from "fileref_factory.hpp" namespace 'TagLib':
    FileRef* make_fileref(str path_obj)