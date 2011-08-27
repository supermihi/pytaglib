# -*- coding: utf-8 -*-
# Copyright 2011 Michael Helmlnig
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation

cimport ctypes, cython
from cython.operator cimport dereference as deref, preincrement as inc

@cython.final
cdef class File:
    """Wrapper class for an audio file with metadata."""
    
    # private C attributes, not visible from within Python
    cdef ctypes.File *_f
    cdef public object tags
    def __cinit__(self, filename):        
        b = filename.encode()
        self._f = ctypes.create(b)
        if not self._f or not self._f.isValid():
            raise OSError('Could not read file {0}'.format(filename))
        
    def __init__(self, filename):
        """Create a new File for the given path, which must exist. Immediately reads metadata."""
        self.tags = dict()
        self._read()
    
    cdef _read(self):
        """Internal method: converts the TagDict of the wrapped File* object into a dict"""
        cdef ctypes.TagDict _tags = self._f.tag().toDict()
        cdef ctypes.mapiter it = _tags.begin()
        cdef ctypes.StringList values
        cdef ctypes.listiter lit
        cdef ctypes.String s
        while it != _tags.end(): # iterate through the keys of the TagDict
            s = deref(it).first # for some reason, <ctypes.pair[...]>deref(it) does not work (bug in Cython?)
            tag = s.toCString(True).decode('UTF-8') # this isn't pretty, but it works
            self.tags[tag] = []
            values = deref(it).second
            lit = values.begin()
            while lit != values.end():
                self.tags[tag].append((<ctypes.String>deref(lit)).toCString(True).decode('UTF-8','replace'))
                inc(lit)
            inc(it)
            
    def save(self):
        """Store the tags that are currently hold in the »tags« attribute into the file. Returns a boolean
        flac which indicates success."""
        if self.readOnly:
            raise OSError('Cannot write tags: file is read-only')
        cdef ctypes.TagDict _tagdict
        cdef ctypes.String s1, s2
        cdef ctypes.Type typ = ctypes.UTF8
        for key, values in self.tags.items():
            x = key.upper().encode() # needed to satisfy Cython; since the String() constructor copies the data, no memory problems should arise here
            s1 = ctypes.String(x,typ)
            if isinstance(values, str):
                values = [ values ]
            for value in values:
                x = value.encode()
                s2 = ctypes.String(x, typ)
                _tagdict[s1].append(s2)
        self._f.tag().fromDict(_tagdict)
        return self._f.save()
        
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