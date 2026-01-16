# -*- coding: utf-8 -*-
# Copyright 2026 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
import pytest

import taglib
from taglib import Picture


def test_picture_dataclass(tiny_png):
    """Test Picture dataclass creation and attributes."""
    pic = Picture(
        data=tiny_png,
        mime_type='image/png',
        description='Test',
        picture_type='Front Cover'
    )
    assert pic.data == tiny_png
    assert pic.mime_type == 'image/png'
    assert pic.description == 'Test'
    assert pic.picture_type == 'Front Cover'
    assert pic.width is None
    assert pic.height is None


def test_picture_defaults(tiny_png):
    """Test Picture dataclass default values."""
    pic = Picture(data=tiny_png, mime_type='image/png')
    assert pic.description == ""
    assert pic.picture_type == "Front Cover"


def test_mp3_pictures_initially_empty(test_file):
    """Test that an MP3 file without cover art has empty pictures list."""
    f = test_file("r2.mp3")
    assert f.pictures == []
    f.close()


def test_mp3_set_and_get_picture(test_data, tiny_png):
    """Test setting and getting a picture in an MP3 file."""
    path = test_data("r2.mp3")

    # Set a picture
    with taglib.File(path) as f:
        f.pictures = [Picture(
            data=tiny_png,
            mime_type='image/png',
            description='Test cover',
            picture_type='Front Cover'
        )]
        f.save()

    # Read it back
    with taglib.File(path) as f:
        assert len(f.pictures) == 1
        pic = f.pictures[0]
        assert isinstance(pic, Picture)
        assert pic.data == tiny_png
        assert pic.mime_type == 'image/png'
        assert pic.description == 'Test cover'
        assert pic.picture_type == 'Front Cover'


def test_mp3_remove_pictures(test_data, tiny_png):
    """Test removing pictures from an MP3 file."""
    path = test_data("r2.mp3")

    # First add a picture
    with taglib.File(path) as f:
        f.pictures = [Picture(
            data=tiny_png,
            mime_type='image/png',
            description='Test',
            picture_type='Front Cover'
        )]
        f.save()

    # Verify it was added
    with taglib.File(path) as f:
        assert len(f.pictures) == 1

    # Remove all pictures
    with taglib.File(path) as f:
        f.remove_pictures()
        f.save()

    # Verify removal
    with taglib.File(path) as f:
        assert f.pictures == []


def test_mp3_multiple_pictures(test_data, tiny_png):
    """Test setting multiple pictures."""
    path = test_data("r2.mp3")

    with taglib.File(path) as f:
        f.pictures = [
            Picture(
                data=tiny_png,
                mime_type='image/png',
                description='Front',
                picture_type='Front Cover'
            ),
            Picture(
                data=tiny_png,
                mime_type='image/png',
                description='Back',
                picture_type='Back Cover'
            )
        ]
        f.save()

    with taglib.File(path) as f:
        assert len(f.pictures) == 2


def test_flac_pictures(test_data, tiny_png):
    """Test pictures in FLAC files."""
    path = test_data("testöü.flac")

    with taglib.File(path) as f:
        f.pictures = [Picture(
            data=tiny_png,
            mime_type='image/png',
            description='FLAC cover',
            picture_type='Front Cover'
        )]
        f.save()

    with taglib.File(path) as f:
        assert len(f.pictures) == 1
        assert f.pictures[0].data == tiny_png


def test_m4a_pictures(test_data, tiny_png):
    """Test pictures in M4A files."""
    path = test_data("issue46.m4a")

    with taglib.File(path) as f:
        f.pictures = [Picture(
            data=tiny_png,
            mime_type='image/png',
            description='',
            picture_type='Front Cover'
        )]
        f.save()

    with taglib.File(path) as f:
        assert len(f.pictures) == 1
        assert f.pictures[0].data == tiny_png


def test_complex_property_keys(test_data, tiny_png):
    """Test that PICTURE appears in complex_property_keys after adding a picture."""
    path = test_data("r2.mp3")

    with taglib.File(path) as f:
        f.pictures = [Picture(
            data=tiny_png,
            mime_type='image/png',
        )]
        f.save()

    with taglib.File(path) as f:
        assert 'PICTURE' in f.complex_property_keys


def test_pictures_empty_list_clears(test_data, tiny_png):
    """Test that setting pictures to empty list removes all pictures."""
    path = test_data("r2.mp3")

    # Add picture
    with taglib.File(path) as f:
        f.pictures = [Picture(data=tiny_png, mime_type='image/png')]
        f.save()

    # Clear with empty list
    with taglib.File(path) as f:
        f.pictures = []
        f.save()

    # Verify cleared
    with taglib.File(path) as f:
        assert f.pictures == []


# Tests migrated from TagLib's C++ test_complexproperties.cpp


def test_read_mp3_picture_compressed(test_file):
    """Test reading picture from MP3 with compressed ID3v2 frames.

    Migrated from TagLib's testReadMp3Picture.
    Note: This test requires TagLib to be built with zlib support.
    """
    f = test_file("compressed_id3_frame.mp3")
    if len(f.pictures) == 0:
        f.close()
        pytest.skip("TagLib built without zlib support for compressed ID3 frames")
    assert len(f.pictures) == 1
    pic = f.pictures[0]
    assert len(pic.data) == 86414
    assert pic.description == ""
    assert pic.mime_type == "image/bmp"
    assert pic.picture_type == "Other"
    f.close()


# Expected picture data from TagLib's has-tags.m4a
_M4A_PNG_DATA = bytes([
    0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00, 0x00, 0x00, 0x0d,
    0x49, 0x48, 0x44, 0x52, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x02,
    0x08, 0x02, 0x00, 0x00, 0x00, 0xfd, 0xd4, 0x9a, 0x73, 0x00, 0x00, 0x00,
    0x16, 0x49, 0x44, 0x41, 0x54, 0x78, 0x9c, 0x63, 0x7c, 0x9f, 0xca, 0xc0,
    0xc0, 0xc0, 0xc0, 0xc4, 0xc0, 0xc0, 0xc0, 0xc0, 0xc0, 0x00, 0x00, 0x11,
    0x09, 0x01, 0x58, 0xab, 0x88, 0xdb, 0x6f, 0x00, 0x00, 0x00, 0x00, 0x49,
    0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82
])

_M4A_JPEG_DATA = bytes([
    0xff, 0xd8, 0xff, 0xe0, 0x00, 0x10, 0x4a, 0x46, 0x49, 0x46, 0x00, 0x01,
    0x01, 0x01, 0x00, 0x64, 0x00, 0x64, 0x00, 0x00, 0xff, 0xdb, 0x00, 0x43,
    0x00, 0x09, 0x06, 0x07, 0x08, 0x07, 0x06, 0x09, 0x08, 0x08, 0x08, 0x0a,
    0x0a, 0x09, 0x0b, 0x0e, 0x17, 0x0f, 0x0e, 0x0d, 0x0d, 0x0e, 0x1c, 0x14,
    0x15, 0x11, 0x17, 0x22, 0x1e, 0x23, 0x23, 0x21, 0x1e, 0x20, 0x20, 0x25,
    0x2a, 0x35, 0x2d, 0x25, 0x27, 0x32, 0x28, 0x20, 0x20, 0x2e, 0x3f, 0x2f,
    0x32, 0x37, 0x39, 0x3c, 0x3c, 0x3c, 0x24, 0x2d, 0x42, 0x46, 0x41, 0x3a,
    0x46, 0x35, 0x3b, 0x3c, 0x39, 0xff, 0xdb, 0x00, 0x43, 0x01, 0x0a, 0x0a,
    0x0a, 0x0e, 0x0c, 0x0e, 0x1b, 0x0f, 0x0f, 0x1b, 0x39, 0x26, 0x20, 0x26,
    0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39,
    0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39,
    0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39,
    0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39, 0x39,
    0x39, 0x39, 0xff, 0xc0, 0x00, 0x11, 0x08, 0x00, 0x02, 0x00, 0x02, 0x03,
    0x01, 0x22, 0x00, 0x02, 0x11, 0x01, 0x03, 0x11, 0x01, 0xff, 0xc4, 0x00,
    0x15, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0xff, 0xc4, 0x00, 0x14,
    0x10, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xc4, 0x00, 0x15, 0x01, 0x01,
    0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x04, 0x06, 0xff, 0xc4, 0x00, 0x14, 0x11, 0x01, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0xff, 0xda, 0x00, 0x0c, 0x03, 0x01, 0x00, 0x02, 0x11,
    0x03, 0x11, 0x00, 0x3f, 0x00, 0x8d, 0x80, 0xb8, 0x19, 0xff, 0xd9
])


def test_read_m4a_multiple_pictures(test_file):
    """Test reading multiple pictures from M4A file.

    Migrated from TagLib's testReadM4aPicture.
    """
    f = test_file("has-tags.m4a")
    assert len(f.pictures) == 2

    # First picture is PNG
    pic1 = f.pictures[0]
    assert pic1.data == _M4A_PNG_DATA
    assert pic1.mime_type == "image/png"

    # Second picture is JPEG
    pic2 = f.pictures[1]
    assert pic2.data == _M4A_JPEG_DATA
    assert pic2.mime_type == "image/jpeg"
    f.close()


def test_read_ogg_picture_with_dimensions(test_file):
    """Test reading picture with extended properties from Ogg file.

    Migrated from TagLib's testReadOggPicture.
    Tests picture metadata including width and height (available for Xiph/FLAC).
    Note: colorDepth and numColors from TagLib are not exposed in pytaglib's Picture API.
    """
    f = test_file("lowercase-fields.ogg")
    assert len(f.pictures) == 1
    pic = f.pictures[0]
    assert pic.data == b"JPEG data"
    assert pic.mime_type == "image/jpeg"
    assert pic.picture_type == "Back Cover"
    assert pic.description == "new image"
    assert pic.width == 5
    assert pic.height == 6
    f.close()


def test_flac_picture_with_dimensions(test_data, tiny_png):
    """Test writing and reading FLAC picture with full metadata.

    Migrated from TagLib's testReadWriteFlacPicture.
    Tests that picture properties (including width and height) are properly
    saved and read back from FLAC files.
    Note: colorDepth and numColors from TagLib are not exposed in pytaglib's Picture API.
    """
    path = test_data("no-tags.flac")

    # Write picture with metadata
    with taglib.File(path) as f:
        assert f.pictures == []
        f.pictures = [Picture(
            data=tiny_png,
            mime_type='image/png',
            description='Embedded cover',
            picture_type='Front Cover',
            width=1,
            height=1,
        )]
        f.save()

    # Read back and verify all properties
    with taglib.File(path) as f:
        assert len(f.pictures) == 1
        pic = f.pictures[0]
        assert pic.data == tiny_png
        assert pic.mime_type == 'image/png'
        assert pic.description == 'Embedded cover'
        assert pic.picture_type == 'Front Cover'
        assert pic.width == 1
        assert pic.height == 1

    # Clear pictures and verify
    with taglib.File(path) as f:
        f.pictures = []
        f.save()

    with taglib.File(path) as f:
        assert f.pictures == []


