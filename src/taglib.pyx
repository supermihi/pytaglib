# -*- coding: utf-8 -*-
# distutils: language = c++
# distutils: libraries = [tag]
# cython: language_level = 3
# Copyright 2011-2015 Michael Helmling, michaelhelmling@posteo.de
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation

from libcpp.utility cimport pair
cimport ctypes, mpeg

version = '1.0.1'

cdef str toUnicode(ctypes.String s):
    """Convert a TagLib::String to unicode python (str in py3k, unicode python2) string."""
    return s.to8Bit(True).decode('UTF-8', 'replace')


cdef dict propertyMapToDict(ctypes.PropertyMap map):
    """Convert a TagLib::PropertyMap to a dict mapping unicode to list of unicode."""
    cdef:
        ctypes.StringList values
        pair[ctypes.String,ctypes.StringList] mapIter
        dict dct = {}
        str tag
    for mapIter in map:
        tag = toUnicode(mapIter.first)
        dct[tag] = []
        values = mapIter.second
        for value in values:
            dct[tag].append(toUnicode(value))
    return dct


cdef class File:
    """Wrapper class for an audio file with metadata.
    
    To read tags from an audio file, simply create a *File* object, passing the file's
    path to the constructor:
    
    >>> f = taglib.File('/path/to/file.ogg')
    
    The tags are stored in the attribute *tags* as a *dict* mapping strings (tag names)
    to lists of strings (tag values).

    If the file contains some metadata that is not supported by pytaglib or not representable
    as strings (e.g. cover art, proprietary data written by some programs, ...), according
    identifiers will be placed into the *unsupported* attribute of the File object. Using the
    method *removeUnsupportedProperties*, some or all of those can be removed.
    
    Additionally, the readonly attributes *length*, *bitrate*, *sampleRate*, and *channels* are
    available with their obvious meanings.
    
    Changes to the *tags* attribute are stored using the *save* method.
    """
    
    cdef:
        ctypes.File *_f
        public dict tags
        readonly object path
        readonly list unsupported
        bint applyMPEGhack

    def __cinit__(self, path, applyID3v2Hack=False):
        if isinstance(path, unicode):
            path_b = path.encode('UTF-8')
        else:
            path_b = path
        self._f = ctypes.create(path_b)
        if not self._f or not self._f.isValid():
            raise OSError('Could not read file "{0}"'.format(path))
        self.applyMPEGhack = False
        if ctypes.TAGLIB_MAJOR_VERSION <= 1 and ctypes.TAGLIB_MINOR_VERSION <= 8 \
                and applyID3v2Hack and len(path_b) >= 4 and path_b[-4:].lower() == b'.mp3':
            print('applying MPEG hack on {}'.format(path))
            self.applyMPEGhack = True

    def __init__(self, path, applyID3v2Hack=False):
        self.tags = dict()
        self.unsupported = list()
        self.path = path
        self._read()

    cdef void _read(self):
        """Convert the PropertyMap of the wrapped File* object into a python dict.
        
        This method is not accessible from Python, and is called only once, immediately after
        object creation.
        """
        
        cdef:
            ctypes.PropertyMap _tags = self._f.properties()
            ctypes.String s
            ctypes.StringList unsupported
        self.tags = propertyMapToDict(_tags)
        unsupported = _tags.unsupportedData()
        for s in unsupported:
            self.unsupported.append(toUnicode(s))

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
            ctypes.PropertyMap cTagdict, cRemaining
            ctypes.String cKey, cValue
        if self.applyMPEGhack:
            (<mpeg.File*>self._f).save(2, False)
        for key, values in self.tags.items():
            if isinstance(key, bytes):
                cKey = ctypes.String(key.upper(), ctypes.UTF8)
            else:
                cKey = ctypes.String(key.upper().encode('UTF-8'), ctypes.UTF8)
            if isinstance(values, bytes) or isinstance(values, unicode):
                # the user has accidentally used a single tag value instead a length-1 list
                values = [ values ]
            for value in values:
                if isinstance(value, bytes):
                    cValue = ctypes.String(value.upper(), ctypes.UTF8)
                else:
                    cValue = ctypes.String(value.encode('UTF-8'), ctypes.UTF8)
                cTagdict[cKey].append(cValue)
        
        cRemaining = self._f.setProperties(cTagdict)
        if self.applyMPEGhack:
            success = (<mpeg.File*>self._f).save(2, True)
        else:
            success = self._f.save()
        if not success:
            raise OSError('Unable to save tags: Unknown OS error')
        return propertyMapToDict(cRemaining)
    
    def removeUnsupportedProperties(self, properties):
        """This is a direct binding for the corresponding TagLib method."""
        cdef ctypes.StringList cProps
        for value in properties:
            cProps.append(ctypes.String(value.encode('UTF-8'), ctypes.UTF8))
        self._f.removeUnsupportedProperties(cProps)
        
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
