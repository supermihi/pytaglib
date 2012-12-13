cimport ctypes


cdef extern from "taglib/id3v2tag.h" namespace "TagLib::ID3v2":
    cdef cppclass Tag

cdef extern from "taglib/mpegfile.h" namespace "TagLib::MPEG":
    cdef cppclass File(ctypes.File):
        Tag* ID3v2Tag(bint)
        bint strip(int)
        bint save(bint, int)
