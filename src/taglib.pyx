cimport ctypes, cython
from cython.operator cimport dereference as deref, preincrement as inc


class TagDict(dict):
    """A somewhat smart dict used for tags. Automatically translates key access to uppercase keys and allows
    for convenience to assign a string instead of a list of strings to a key, in which case it will be converted
    into a list containing the string as its sole element.
    
    The checks performed by this class are far from complete to ensuere a valid setting for the audio metadata.
    Users of this library should not rely on this features, but rather make sure on their own that keys are
    uppercase ASCII strings and values are lists of strings, or single strings."""
    
    def __getitem__(self, key):
        if not isinstance(key, str):
            raise KeyError("Tag keys must be strings")
        return dict.__getitem__(self, key.upper())
        
    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise KeyError("Tag keys must be strings")
        key = key.upper()
        if not isinstance(value, list):
            if not isinstance(value, str):
                raise ValueError("Tag value must be a list of strings or a single string")
            else:
                dict.__setitem__(self, key, [value])
        else:
            dict.__setitem__(self, key, value)
            
@cython.final
cdef class File:
    """Wrapper class for an audio file with metadata."""
    
    # private C attributes, not visible from within Python
    cdef ctypes.File *_f
    cdef object _tags
    
    def __cinit__(self, filename):        
        b = filename.encode()
        self._f = ctypes.create(b)
        if not self._f:
            raise OSError('Could not read file {0}'.format(filename))
        
    def __init__(self, filename):
        """Create a new File for the given path, which must exist. Immediately reads metadata."""
        self._tags = TagDict()
        self._read()
    
    cdef _read(self):
        """Internal method: converts the TagDict of the wrapped File* object into a dict"""
        cdef ctypes.TagDict _tags = self._f.tag().toDict()
        cdef ctypes.mapiter it = _tags.begin()
        cdef ctypes.StringList liste
        cdef ctypes.listiter lit
        cdef ctypes.String s
        while it != _tags.end(): # iterate through the keys of the UTagDict
            s = deref(it).first # for some reason, <ctypes.pair[...]>deref(it) does not work (bug in Cython?)
            tag = s.toCString(True).decode('UTF-8') # this is ugly, but works
            self._tags[tag] = []
            liste = deref(it).second
            lit = liste.begin()
            while lit != liste.end():
                wert = (<ctypes.String>deref(lit)).toCString(True).decode('UTF-8','replace')
                self._tags[tag].append(wert)
                inc(lit)
            inc(it)
            
    def save(self):
        """Store the tags that are currently hold in the »tags« attribute into the file. You should check the
        readOnly attribute before calling this function."""
        cdef ctypes.TagDict _tagdict
        cdef ctypes.String s
        cdef ctypes.String s2
        cdef ctypes.Type typ = ctypes.UTF8
        for key in self._tags:
            x = key.encode() # needed to satisfy Cython; since the String() constructor copies the data, no memory problems should arise here
            s = ctypes.String(x,typ) 
            for value in self._tags[key]:
                y = value.encode()
                s2 = ctypes.String(y, typ)
                _tagdict[s].append(s2)
        self._f.tag().fromDict(_tagdict)
        return self._f.save()
        
    def __dealloc__(self):
        del self._f       
             
    property tags:
        """The TagDict which stores the tags."""
        def __get__(self):
            return self._tags
        def __set__(self, value):
            """Perform some basic checks (not exhaustive) if a valid tag dict is passed"""
            if not isinstance(value, dict):
                raise ValueError("tags attribute must be a dict")
            for key in value:
                if not isinstance(key, str):
                    raise KeyError("tag keys must be str")
                if not key.isUpper():
                    raise KeyError("tag keys must be upper keys")
                if not isinstance(value[key], list):
                    raise KeyError("tag values must be lists")
            self._tags = value
        def __del__(self):
            self._tags = TagDict()
            
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