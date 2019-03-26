# -*- coding: utf-8 -*-
# Copyright 2019 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
from __future__ import unicode_literals

import os, stat, sys
import taglib

import pytest

from . import copy_test_file


def test_not_existing_file_raises():
    """Ensure OSError is raised if a file does not exist, or is a directory."""
    with pytest.raises(OSError):
        taglib.File('/this/file/almost/certainly/does/not/exist.flac')
    with pytest.raises(OSError):
        taglib.File('/spæciäl/chàracterß.mp3')
    with pytest.raises(OSError):
        taglib.File('/usr')  # directory
    with pytest.raises(OSError):
        taglib.File("/nonexistent.ogg")


def test_os_error_on_save_read_only_file(tmpdir):
    """Ensure OSError is raised when save() is called on read-only files."""
    if os.getuid() == 0:
        pytest.skip('taglib allows writing read-only files as root')
    f = copy_test_file('rare_frames.mp3', tmpdir)
    os.chmod(f, stat.S_IREAD)
    tf = taglib.File(f)
    assert tf.readOnly
    with pytest.raises(OSError):
        tf.save()
    os.chmod(f, stat.S_IREAD & stat.S_IWRITE)
    tf.close()


def test_file_with_non_ascii_name_throws_on_readonly_save(tmpdir):
    """Motivated by https://github.com/supermihi/pytaglib/issues/21.
    """
    if os.getuid() == 0:
        pytest.skip('taglib allows writing read-only files as root')
    copy_file = copy_test_file('readönly.mp3', tmpdir)
    os.chmod(copy_file, stat.S_IREAD)
    tfile = taglib.File(copy_file.encode('utf8'))
    tfile.tags['COMMENT'] = ['']
    with pytest.raises(OSError):
        tfile.save()
    tfile.close()


def test_can_read_bytes_filename_non_ascii(tmpdir):
    f = copy_test_file('testöü.flac', tmpdir)
    tf = taglib.File(f.encode('utf8'))
    tf.close()


def test_can_read_unicode_filename_non_ascii(tmpdir):
    f = copy_test_file('testöü.flac', tmpdir)
    if sys.version_info.major == 2:
        f = unicode(f)
    tf = taglib.File(f)
    tf.close()
