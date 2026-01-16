# -*- coding: utf-8 -*-
# Copyright 2021 Michael Helmling, michaelhelmling@posteo.de
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
from libcpp cimport bool as cppbool
from libcpp.utility cimport pair

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
