# -*- coding: utf-8 -*-
# Copyright 2011-2012 Michael Helmling, helmling@mathematik.uni-kl.de
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
from __future__ import print_function, unicode_literals
cimport ctypes, cython
from libcpp.string cimport string
from cython.operator cimport dereference as deref, preincrement as inc

cdef object tounicode(ctypes.String s):
    """Convert a TagLib::String object to unicode python (str in python3, uncode python2) string."""
    cdef string cppstr = s.to8Bit(True)
    cdef bytes bstr = cppstr.c_str() # necessary to avoid compilation error due to "const" violation
    return bstr.decode('UTF-8', 'replace')

@cython.final
cdef class File:
    """Wrapper class for an audio file with metadata.
    
    To read tags from an audio file, simply create a *File* object, passing the file's
    path to the constructor:
    
    f = taglib.File("/path/to/file.ogg")
    
    The tags are stored in the attribute *tags* as a *dict* mapping strings (tag names)
    to lists of strings (tag values).
    
    Additionally, the readonly attributes "length", "bitrate", "sampleRate", and
    "channels" are available.
    
    Changes to the *tags* attribute are saved using the *save* method, which returns a
    bool value indicating success.
    
    Information about tags which are not representable by the "tag name"->"list of values"
    model is stored in the attribute *unsupported*, which is a list of strings. For example,
    in case of ID3 tags, the list contains the ID3 frame IDs of unsupported frames. Such
    unsupported metadata can be removed by passing (a subset of) the *unsupported* list
    to *removeUnsupportedProperties*. See the TagLib documentation for details. 
    """
    
    cdef ctypes.File *_f
    cdef public object tags
    cdef public object unsupported
    cdef public object path
    
    def __cinit__(self, path):
        path_b = path.encode('UTF-8')
        self._f = ctypes.create(path_b)
        if not self._f or not self._f.isValid():
            
            raise OSError('Could not read file "{0}"'.format(path))
        
    def __init__(self, path):
        """Create a new File for the given path, which must exist. Immediately reads metadata."""
        self.tags = dict()
        self.unsupported = list()
        self.path = path
        self._read()
    
    cdef _read(self):
        """Convert the PropertyMap of the wrapped File* object into a python dict.
        
        This method is not accessible from Python, and is called only once, immediately after
        object creation."""
        cdef ctypes.PropertyMap _tags = self._f.properties()
        cdef ctypes.mapiter it = _tags.begin()
        cdef ctypes.StringList values
        cdef ctypes.listiter lit
        cdef ctypes.String s
        cdef char* cstr
        cdef bytes bstr
        while it != _tags.end(): # iterate through the keys of the PropertyMap
            s = deref(it).first # for some reason, <ctypes.pair[...]>deref(it) does not work (bug in Cython?)
            tag = tounicode(s)
            self.tags[tag] = []
            values = deref(it).second
            lit = values.begin()
            while lit != values.end():
                self.tags[tag].append(tounicode(<ctypes.String>deref(lit)))
                inc(lit)
            inc(it)
            
        lit = _tags.unsupportedData().begin()
        while lit != _tags.unsupportedData().end():
            s = deref(lit)
            self.unsupported.append(tounicode(s))
            inc(lit)
    
    def save(self):
        """Store the tags currently hold in the *tags* attribute into the file. Returns a boolean
        flag which indicates success."""
        if self.readOnly:
            raise OSError('Unable to save tags: file "{0}" is read-only'.format(self.path))
        cdef ctypes.PropertyMap _tagdict
        cdef ctypes.String s1, s2
        cdef ctypes.Type typ = ctypes.UTF8
        for key, values in self.tags.items():
            x = key.upper().encode() # needed to satisfy Cython; since the String() constructor copies the data, no memory problems should arise here
            s1 = ctypes.String(x,typ)
            if isinstance(values, str):
                values = [ values ]
            for value in values:
                x = value.encode('utf-8')
                s2 = ctypes.String(x, typ)
                _tagdict[s1].append(s2)
        cdef ctypes.PropertyMap remaining = self._f.setProperties(_tagdict)
        print(remaining.size())
        return self._f.save()
    
    def removeUnsupportedProperties(self, properties):
        """This is a direct binding for the corresponding TagLib method."""
        cdef ctypes.StringList _props
        cdef ctypes.String s
        cdef ctypes.Type typ = ctypes.UTF8
        for value in properties:
            x = value.encode('utf-8')
            s = ctypes.String(x, typ)
            _props.append(s)
        self._f.removeUnsupportedProperties(_props)
        
    def __dealloc__(self):
        del self._f       
        
    property length:
        def __get__(self):
            return self._f.audioProperties().length()
            
    property bitrate:
        def __get__(self):
            return self._f.audioProperties().bitrate()
    
    property sampleRate:
        def __get__(self):
            return self._f.audioProperties().sampleRate()
            
    property channels:
        def __get__(self):
            return self._f.audioProperties().channels()
    
    property readOnly:
        def __get__(self):
            return self._f.readOnly()