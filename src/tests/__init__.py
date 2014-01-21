# -*- coding: utf-8 -*-
# Copyright 2011-2014 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
from contextlib import contextmanager
import os.path, shutil, tempfile

@contextmanager
def copyTestFile(name):
    """Make a temporary copy of test data file *name* (without dir) and return its full path. The file
    is deleted on exit."""
    orig_file = os.path.join(os.path.dirname(__file__), 'data', name)
    tempdir = tempfile.mkdtemp()
    copy_file = os.path.join(tempdir, name)
    shutil.copy(orig_file, copy_file)
    print(tempdir)
    try:
        yield copy_file
    finally:
        shutil.rmtree(tempdir)
    
