# -*- coding: utf-8 -*-
# Copyright 2011-2017 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
from __future__ import absolute_import, unicode_literals

import taglib
import os
import stat

import pytest

from tests import copy_test_file


@pytest.mark.skipIf(os.getuid() == 0, 'taglib allows writing read-only files as root')
def test_file_with_non_ascii_name_throws_on_readonly_save(tmpdir):
    """Motivated by https://github.com/supermihi/pytaglib/issues/21.
    """
    copy_file = copy_test_file('readönly.mp3', tmpdir)
    os.chmod(copy_file, stat.S_IREAD)
    tfile = taglib.File(copy_file.encode('utf8'))
    tfile.tags['COMMENT'] = ['']
    with pytest.raises(OSError):
        tfile.save()
    tfile.close()
