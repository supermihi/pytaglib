# -*- coding: utf-8 -*-
# Copyright 2019 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
from __future__ import unicode_literals

import os, stat
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


@pytest.mark.skipif(os.getuid() == 0, reason='taglib allows writing read-only files as root')
def test_os_error_on_save_read_only_file(tmpdir):
    """Ensure OSError is raised when save() is called on read-only files."""
    f = copy_test_file('rare_frames.mp3', tmpdir)
    os.chmod(f, stat.S_IREAD)
    tf = taglib.File(f)
    assert tf.readOnly
    with pytest.raises(OSError):
        tf.save()
    os.chmod(f, stat.S_IREAD & stat.S_IWRITE)
    tf.close()
