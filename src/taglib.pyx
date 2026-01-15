# -*- coding: utf-8 -*-
# distutils: language = c++
# Copyright 2021 Michael Helmling, michaelhelmling@posteo.de
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation

from libcpp cimport bool as cppbool
from libcpp.utility cimport pair
from pathlib import Path
cimport ctypes

version = '3.1.0'

cdef str toStr(ctypes.String s):
    """Converts TagLib::String to a Python str."""
    return s.to8Bit(True).decode('UTF-8', 'replace')

cdef ctypes.String toCStr(value: str | bytes):
    """Convert a Python string or bytes to TagLib::String"""
    if isinstance(value, str):
        value = value.encode('UTF-8')
    return ctypes.String(value, ctypes.UTF8)

cdef dict[str, str] propertyMapToDict(ctypes.PropertyMap map):
    """Convert a TagLib::PropertyMap to a dict mapping unicode string to list of unicode strings."""
    cdef:
        ctypes.StringList values
        pair[ctypes.String, ctypes.StringList] mapIter
        dict dct = {}
        str tag
    for mapIter in map:
        tag = toStr(mapIter.first)
        dct[tag] = []
        values = mapIter.second
        for value in values:
            dct[tag].append(toStr(value))
    return dct

cdef bytes bytevector_to_bytes(ctypes.ByteVector bv):
    """Convert TagLib::ByteVector to Python bytes."""
    return bv.data()[:bv.size()]

cdef ctypes.ByteVector bytes_to_bytevector(bytes data):
    """Convert Python bytes to TagLib::ByteVector."""
    return ctypes.ByteVector(data, len(data))

cdef object variant_to_object(ctypes.Variant v):
    """Convert a TagLib::Variant to a Python object."""
    cdef:
        cppbool ok = False
    if v.type() == ctypes.Void:
        return None
    elif v.type() == ctypes.Bool:
        return v.toBool(&ok)
    elif v.type() == ctypes.Int:
        return v.toInt(&ok)
    elif v.type() == ctypes.UInt:
        return v.toUInt(&ok)
    elif v.type() == ctypes.VString:
        return toStr(v.toString(&ok))
    elif v.type() == ctypes.VByteVector:
        return bytevector_to_bytes(v.toByteVector(&ok))
    elif v.type() == ctypes.VVariantMap:
        return variant_map_to_dict(v.toMap(&ok))
    else:
        return None

cdef dict variant_map_to_dict(ctypes.VariantMap vm):
    """Convert a TagLib::VariantMap to a Python dict."""
    cdef:
        pair[ctypes.String, ctypes.Variant] mapIter
        dict result = {}
    for mapIter in vm:
        result[toStr(mapIter.first)] = variant_to_object(mapIter.second)
    return result

cdef list variant_map_to_list(ctypes.List[ctypes.VariantMap] vl):
    """Convert a TagLib::List<VariantMap> to a Python list of dicts."""
    cdef:
        ctypes.VariantMap vm
        list result = []
    for vm in vl:
        result.append(variant_map_to_dict(vm))
    return result

cdef ctypes.Variant object_to_variant(object obj):
    """Convert a Python object to a TagLib::Variant."""
    cdef:
        ctypes.VariantMap vm
        ctypes.String cstr
        ctypes.ByteVector bv
        int intval
    if obj is None:
        return ctypes.Variant()
    elif isinstance(obj, bool):
        # bool must be checked before int since bool is subclass of int
        intval = 1 if obj else 0
        return ctypes.Variant(intval)
    elif isinstance(obj, int):
        intval = obj
        return ctypes.Variant(intval)
    elif isinstance(obj, str):
        cstr = toCStr(obj)
        return ctypes.Variant(cstr)
    elif isinstance(obj, bytes):
        bv = bytes_to_bytevector(obj)
        return ctypes.Variant(bv)
    elif isinstance(obj, dict):
        vm = dict_to_variant_map(obj)
        return ctypes.Variant(vm)
    else:
        return ctypes.Variant()

cdef ctypes.VariantMap dict_to_variant_map(dict d):
    """Convert a Python dict to a TagLib::VariantMap."""
    cdef:
        ctypes.VariantMap vm
        ctypes.String key
    for k, v in d.items():
        key = toCStr(k)
        vm[key] = object_to_variant(v)
    return vm

cdef ctypes.List[ctypes.VariantMap] list_to_ariant_map_list(list lst):
    """Convert a Python list of dicts to a TagLib::List<VariantMap>."""
    cdef:
        ctypes.List[ctypes.VariantMap] result
    for item in lst:
        result.append(dict_to_variant_map(item))
    return result

cdef class File:
    """Class representing an audio file with metadata ("tags").

    To read tags from an audio file, create a *File* object, passing the file's path to the
    constructor (should be a unicode string):

    >>> f = taglib.File('/path/to/file.ogg')

    The tags are stored in the attribute *tags* as a *dict* mapping strings (tag names)
    to lists of strings (tag values).

    >>> for tag, values in f:
    >>>     print('{}->{}'.format(tag, ', '.join(values)))

    If the file contains some metadata that is not supported by pytaglib or not representable
    as strings (e.g. cover art, proprietary data written by some programs, ...), according
    identifiers will be placed into the *unsupported* attribute of the File object. Using the
    method *removeUnsupportedProperties*, some or all of those can be removed.

    Additionally, the readonly attributes *length*, *bitrate*, *sampleRate*, and *channels* are
    available with their obvious meanings.

    >>> print('File length: {}'.format(f.length))

    Changes to the *tags* attribute are stored using the *save* method.

    >>> f.save()
    """
    cdef ctypes.FileRef *cFile
    cdef public dict[str | bytes, str | bytes] tags
    cdef readonly object path
    cdef readonly list unsupported
    cdef readonly object save_on_exit

    def __cinit__(self, path, save_on_exit: bool = False):
        if not isinstance(path, Path):
            if isinstance(path, bytes):
                path = path.decode('utf-8')
            path = Path(path)
        self.path = path
        self.cFile = ctypes.make_fileref(str(path))
        if self.cFile is NULL or self.cFile.file() is NULL or not self.cFile.file().isValid():
            raise OSError(f'Could not read file {path}')

    def __init__(self, path: Path | str | bytes, save_on_exit: bool = False) -> None:
        self.tags = dict()
        self.unsupported = list()
        self.readProperties()
        self.save_on_exit = save_on_exit

    cdef void readProperties(self):
        """Convert the Taglib::PropertyMap of the wrapped Taglib::File object into a python dict.

        This method is not accessible from Python, and is called only once, immediately after
        object creation.
        """

        cdef:
            ctypes.PropertyMap cTags = self.cFile.properties()
            ctypes.String cString
            ctypes.StringList unsupported
        self.tags = propertyMapToDict(cTags)
        unsupported = cTags.unsupportedData()
        for cString in unsupported:
            self.unsupported.append(toStr(cString))

    def save(self) -> dict[str, str]:
        """Store the tags currently hold in the `tags` attribute into the file.

        If some tags cannot be stored because the underlying metadata format does not support them,
        the unsuccesful tags are returned as a "sub-dictionary" of `self.tags` which will be empty
        if everything is ok.

        Raises
        ------
        OSError
            If the save operation fails completely (file does not exist, insufficient rights, ...).
        ValueError
            When attempting to save after the file was closed.
        """
        self.check_writable()
        cdef:
            ctypes.PropertyMap cTagdict, cRemaining
            ctypes.String cKey, cValue

        # populate cTagdict with the contents of self.tags
        for key, values in self.tags.items():
            cKey = toCStr(key.upper())
            if isinstance(values, (bytes, str)):
                # the user has accidentally used a single tag value instead a length-1 list
                values = [ values ]
            for value in values:
                cTagdict[cKey].append(toCStr(value))

        cRemaining = self.cFile.setProperties(cTagdict)
        success = self.cFile.save()
        if not success:
            raise OSError('Unable to save tags: Unknown OS error')
        return propertyMapToDict(cRemaining)

    def removeUnsupportedProperties(self, properties):
        """This is a direct binding for the corresponding TagLib method."""
        if not self.cFile:
            raise ValueError('I/O operation on closed file.')
        cdef ctypes.StringList cProps
        for value in properties:
            cProps.append(toCStr(value))
        self.cFile.removeUnsupportedProperties(cProps)

    def close(self):
        """Closes the file by deleting the underlying Taglib::File object. This will close any open
        streams. Calling methods like `save()` or the read-only properties after `close()` will
        raise an exception."""
        if self.is_closed:
            raise ValueError("File already closed")
        del self.cFile
        self.cFile = NULL

    def __dealloc__(self):
        if self.cFile:
            del self.cFile

    @property
    def is_closed(self) -> bool:
        return self.cFile is NULL

    @property
    def length(self) -> float:
        self.check_closed()
        return self.cFile.audioProperties().lengthInMilliseconds() / 1_000.0

    @property
    def bitrate(self) -> int:
        self.check_closed()
        return self.cFile.audioProperties().bitrate()

    @property
    def sampleRate(self) -> int:
        self.check_closed()
        return self.cFile.audioProperties().sampleRate()

    @property
    def channels(self) -> int:
        self.check_closed()
        return self.cFile.audioProperties().channels()

    @property
    def readOnly(self) -> bool:
        self.check_closed()
        return self.cFile.file().readOnly()

    cdef void check_closed(self):
        if self.is_closed:
            raise ValueError('I/O operation on closed file.')

    cdef void check_writable(self) -> None:
        if self.readOnly:
            raise OSError(f'File is read-only.')

    def __enter__(self) -> File:
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        if self.save_on_exit:
            self.save()
        self.close()

    def __repr__(self) -> str:
        return f"File('{self.path}')"



def taglib_version() -> tuple[int, int]:
    """Taglib major and minor version, as 2-tuple.

    Note: this is the version used for compiling the Cython module. Under certain
    circumstances (e.g. dynamic linking, or re-using the cythonized code after
    upgrading Taglib) the actually running Taglib version might be different.
    """
    return ctypes.TAGLIB_MAJOR_VERSION, ctypes.TAGLIB_MINOR_VERSION
