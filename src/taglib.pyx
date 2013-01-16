# -*- coding: utf-8 -*-
# distutils: language = c++
# distutils: libraries = [tag, stdc++]
# Copyright 2011-2013 Michael Helmling, michaelhelmling@posteo.de
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation

from __future__ import print_function, unicode_literals

import sys

cimport cython
from libcpp.string cimport string
from cython.operator cimport dereference as deref, preincrement as inc

cimport ctypes, mpeg

version = "0.3.4"

cdef object tounicode(ctypes.String s):
    """Convert a TagLib::String to unicode python (str in py3k, unicode python2) string."""
    
    cdef string cppstr = s.to8Bit(True)
    cdef bytes bstr = cppstr.c_str() # avoids compilation error due to "const" violation
    return bstr.decode('UTF-8', 'replace')


cdef object todict(ctypes.PropertyMap map):
    """Convert a TagLib::PropertyMap to a dict mapping unicode to list of unicode."""
    cdef:
        ctypes.StringList values
        ctypes.listiter lit
        ctypes.String s
        ctypes.mapiter it = map.begin()
    dct = dict()
    while it != map.end():
        s = deref(it).first # for some reason, <ctypes.pair[...]>deref(it) does not work
        tag = tounicode(s)
        dct[tag] = []
        values = deref(it).second
        lit = values.begin()
        while lit != values.end():
            dct[tag].append(tounicode(<ctypes.String>deref(lit)))
            inc(lit)
        inc(it)
    return dct


@cython.final
cdef class File:
    """Wrapper class for an audio file with metadata.
    
    To read tags from an audio file, simply create a *File* object, passing the file's
    path to the constructor:
    
    f = taglib.File("/path/to/file.ogg")
    
    The tags are stored in the attribute *tags* as a *dict* mapping strings (tag names)
    to lists of strings (tag values).

    If the file contains some metadata that is not supported by pytaglib or not representable
    as strings (e.g. cover art, proprietary data written by some programs, ...), according
    identifiers will be placed into the *unsupported* attribute of the File object. Using the
    method *removeUnsupportedProperties*, some or all of those can be removed.
    
    Additionally, the readonly attributes "length", "bitrate", "sampleRate", and
    "channels" are available.
    
    Changes to the *tags* attribute are saved using the *save* method.
    """
    
    cdef:
        ctypes.File *_f
        public object tags
        public object path
        public object unsupported
        bint isMPEG
   
 
    def __cinit__(self, path, applyID3v2Hack=False):
        if sys.version_info.major == 3 or isinstance(path, unicode):
            path_b = path.encode('UTF-8')
        else:
            path_b = path
        self._f = ctypes.create(path_b)
        if not self._f or not self._f.isValid():
            raise OSError('Could not read file "{0}"'.format(path))
        
        if applyID3v2Hack and len(path_b) >= 4 and path_b[-4:].lower() == b".mp3":
            print('applying MPEG hack')
            self.isMPEG = True
        else:
            self.isMPEG = False
    

    def __init__(self, path, applyID3v2Hack=False):
        """Create a new File for the given path and read metadata.

        If the path does not exist or cannot be opened, an OSError will be raised.
        """
        
        self.tags = dict()
        self.unsupported = list()
        self.path = path
        self._read()
        
    

    cdef _read(self):
        """Convert the PropertyMap of the wrapped File* object into a python dict.
        
        This method is not accessible from Python, and is called only once, immediately after
        object creation.
        """
        
        cdef:
            ctypes.PropertyMap _tags = self._f.properties()
            ctypes.listiter lit
            ctypes.String s
        self.tags = todict(_tags)

        lit = _tags.unsupportedData().begin()
        while lit != _tags.unsupportedData().end():
            s = deref(lit)
            self.unsupported.append(tounicode(s))
            inc(lit)
   
 
    def save(self):
        """Store the tags currently hold in the *tags* attribute into the file.
        
        If some tags could not be stored because the underlying metadata format does not
        support them, the unsuccesful tags are returned as a "subdict" of self.tags which
        will be empty if everything is ok.
        If the save operation completely fails (file does not exist, insufficient rights),
        an OSError is raised.
        """
        
        if self.readOnly:
            raise OSError('Unable to save tags: file "{0}" is read-only'.format(self.path))
        cdef:
            ctypes.PropertyMap _tagdict, _remaining
            ctypes.String s1, s2
        if self.isMPEG:
            (<mpeg.File*>self._f).save(2, False)
        for key, values in self.tags.items():
            x = key.upper().encode('utf-8')
            s1 = ctypes.String(x, ctypes.UTF8)
            if isinstance(values, str):
                values = [ values ]
            for value in values:
                x = value.encode('utf-8')
                s2 = ctypes.String(x, ctypes.UTF8)
                _tagdict[s1].append(s2)
        
        _remaining = self._f.setProperties(_tagdict)
        if self.isMPEG:
            success = (<mpeg.File*>self._f).save(2, True)
        else:
            success = self._f.save()
        if not success:
            raise OSError("Unable to save tags: Unknown OS error")
        return todict(_remaining)
    
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
        
    def __repr__(self):
        return "File('{}')".format(self.path)
