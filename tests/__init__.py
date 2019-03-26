# -*- coding: utf-8 -*-
# Copyright 2019 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#

import os.path, shutil


def copy_test_file(filename, tmpdir):
    """Make a temporary copy of test data file *name* (without dir) and return its full path."""
    source = os.path.join(os.path.dirname(__file__), 'data', filename)
    target = os.path.join(tmpdir, filename)
    shutil.copyfile(source, target)
    return target
