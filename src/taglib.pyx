# -*- coding: utf-8 -*-
# distutils: language = c++
# Copyright 2021 Michael Helmling, michaelhelmling@posteo.de
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Optional, Union

from pathlib import Path
cimport ctypes

include "_cdef_helpers.pxi"

version = '3.1.0'

Variant = Union[None, bool, int, bytes, "VariantMap"]
VariantMap = Mapping[str, Variant]


@dataclass(slots=True)
class Picture:
    """Represents an embedded picture (cover art) in an audio file.

    Attributes
    ----------
    data : bytes
        The raw image data (e.g., JPEG or PNG bytes)
    mime_type : str
        MIME type of the image (e.g., "image/jpeg", "image/png")
    description : str
        Optional description of the picture (default: "")
    picture_type : str
        Type of picture (default: "Front Cover"). Common values:
        "Front Cover", "Back Cover", "Artist", "Band", etc.
    width : int or None
        Image width in pixels (may be None, mainly available for FLAC)
    height : int or None
        Image height in pixels (may be None, mainly available for FLAC)

    Example
    -------
    >>> # Create a picture from a file
    >>> with open('cover.jpg', 'rb') as img:
    ...     pic = taglib.Picture(
    ...         data=img.read(),
    ...         mime_type='image/jpeg',
    ...         description='Album artwork',
    ...         picture_type='Front Cover'
    ...     )
    """
    data: bytes
    mime_type: str
    description: str = ""
    picture_type: str = "Front Cover"
    width: Optional[int] = None
    height: Optional[int] = None

    def _to_variant_map(self) -> VariantMap:
        """Convert to dictionary format for TagLib."""
        d = {
            'data': self.data,
            'mimeType': self.mime_type,
            'description': self.description,
            'pictureType': self.picture_type,
        }
        if self.width is not None:
            d['width'] = self.width
        if self.height is not None:
            d['height'] = self.height
        return d

    @classmethod
    def _from_variant_map(cls, d: VariantMap) -> 'Picture':
        """Create Picture from dictionary returned by TagLib."""
        return cls(
            data=d.get('data', b''),
            mime_type=d.get('mimeType', ''),
            description=d.get('description', ''),
            picture_type=d.get('pictureType', 'Front Cover'),
            width=d.get('width'),
            height=d.get('height'),
        )


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
                values = [values]
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

    @property
    def complex_property_keys(self) -> Sequence[str]:
        """Get the keys of complex properties (e.g., "PICTURE" for cover art).

        Complex properties are metadata that cannot be represented as simple strings,
        such as embedded cover art images.

        Returns
        -------
        The available complex property keys. Common keys include "PICTURE" for embedded cover art.
        """
        self.check_closed()
        cdef:
            ctypes.StringList keys = self.cFile.complexPropertyKeys()
            ctypes.String key
        for key in keys:
            yield toStr(key)

    def complex_properties(self, key: str) -> Sequence[VariantMap]:
        """Get complex properties for a given key (e.g., "PICTURE").

        Raises ValueError if the file is closed.
        """
        self.check_closed()
        cdef ctypes.List[ctypes.VariantMap] props = self.cFile.complexProperties(toCStr(key))
        return variant_map_to_list(props)

    def set_complex_properties(self, key: str, value: list[VariantMap]) -> bool:
        """Set complex properties for a given key (e.g., "PICTURE").

        Pass an empty list to remove all complex properties for the key.
        Raises ValueError if closed, OSError if read-only.
        """
        self.check_writable()
        cdef ctypes.List[ctypes.VariantMap] cProps = list_to_ariant_map_list(value)
        return self.cFile.setComplexProperties(toCStr(key), cProps)

    @property
    def pictures(self) -> list[Picture]:
        """Get embedded pictures (cover art) from the file.

        Returns
        -------
        list[Picture]
            List of Picture objects, empty if no pictures embedded.
        """
        return [Picture._from_variant_map(d) for d in self.complex_properties('PICTURE')]

    @pictures.setter
    def pictures(self, value: list[Picture]) -> None:
        """Set embedded pictures (cover art) in the file.

        Set to an empty list to remove all pictures.

        Note: Call save() after setting pictures to write changes to disk.

        Parameters
        ----------
        value : list[Picture]
            List of Picture objects

        Example
        -------
        >>> f = taglib.File('song.mp3')
        >>> with open('cover.jpg', 'rb') as img:
        ...     f.pictures = [taglib.Picture(
        ...         data=img.read(),
        ...         mime_type='image/jpeg',
        ...         picture_type='Front Cover'
        ...     )]
        >>> f.save()
        """
        self.set_complex_properties('PICTURE', [p._to_variant_map() for p in value])

    def remove_pictures(self) -> bool:
        """Remove all embedded pictures from the file.

        Note: Call save() after removing pictures to write changes to disk.

        Returns
        -------
        bool
            True if the operation succeeded

        Example
        -------
        >>> f = taglib.File('song.mp3')
        >>> f.remove_pictures()
        >>> f.save()
        """
        return self.set_complex_properties('PICTURE', [])

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

    cdef void check_writable(self):
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
