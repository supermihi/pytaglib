# -*- coding: utf-8 -*-
# Copyright 2019 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#

import os
import stat
import sys
from pathlib import Path

import pytest
import taglib


def test_not_existing_file_raises(tmpdir, tmp_path):
    """Ensure OSError is raised if a file does not exist, or is a directory."""
    with pytest.raises(OSError):
        taglib.File("/this/file/almost/certainly/does/not/exist.flac")
    with pytest.raises(OSError):
        taglib.File("/spæciäl/chàracterß.mp3")
    with pytest.raises(OSError):
        taglib.File("/nonexistent.ogg")
    with pytest.raises(OSError):
        taglib.File(tmpdir)  # directory as string
    with pytest.raises(OSError):
        taglib.File(tmp_path)  # directory as Path


@pytest.mark.skipif(sys.platform == "win32", reason="getuid() only on windows")
def test_os_error_on_save_read_only_file(test_data):
    """Ensure OSError is raised when save() is called on read-only files."""
    if os.getuid() == 0:
        pytest.skip("taglib allows writing read-only files as root")
    f = test_data("rare_frames.mp3")
    os.chmod(f, stat.S_IREAD)
    tf = taglib.File(f)
    assert tf.readOnly
    with pytest.raises(OSError):
        tf.save()
    os.chmod(f, stat.S_IREAD & stat.S_IWRITE)
    tf.close()


@pytest.mark.skipif(sys.platform == "win32", reason="getuid() only on windows")
def test_file_with_non_ascii_name_throws_on_readonly_save(test_data):
    """Motivated by https://github.com/supermihi/pytaglib/issues/21."""
    if os.getuid() == 0:
        pytest.skip("taglib allows writing read-only files as root")
    file = test_data("readönly.mp3")
    os.chmod(file, stat.S_IREAD)
    tfile = taglib.File(str(file).encode("utf8"))
    tfile.tags["COMMENT"] = [""]
    with pytest.raises(OSError):
        tfile.save()
    tfile.close()


@pytest.mark.parametrize(
    "path_map",
    [lambda f: str(f).encode("utf8"), str, lambda f: f],
    ids=["bytes", "unicode string", "Path"],
)
def test_can_read_bytes_filename_non_ascii(test_data, path_map):
    f = test_data("testöü.flac")
    tf = taglib.File(path_map(f))
    assert isinstance(tf.path, Path)
    tf.close()
