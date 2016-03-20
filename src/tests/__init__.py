# -*- coding: utf-8 -*-
# Copyright 2011-2015 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
from contextlib import contextmanager
import os.path, shutil, tempfile

def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

@contextmanager
def copyTestFile(name):
    """Make a temporary copy of test data file *name* (without dir) and return its full path. The file
    is deleted on exit."""
    orig_file = os.path.join(os.path.dirname(__file__), 'data', name)
    tempdir = tempfile.mkdtemp()
    copy_file = os.path.join(tempdir, name)
    shutil.copyfile(orig_file, copy_file)
    try:
        yield copy_file
    finally:
        shutil.rmtree(tempdir, onerror=onerror)
