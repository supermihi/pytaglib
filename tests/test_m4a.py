# -*- coding: utf-8 -*-
# Copyright 2011-2016 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
from __future__ import absolute_import, unicode_literals

import taglib

from tests import copy_test_file


def test_m4a_supports_albumartist(tmpdir):
    """Motivated by https://github.com/supermihi/pytaglib/issues/46.
        """
    copy_file = copy_test_file('issue46.m4a', tmpdir)
    tfile = taglib.File(copy_file)
    assert 'ALBUMARTIST' in tfile.tags
    assert ['Higginbottom, Edward'] == tfile.tags['ALBUMARTIST']
    tfile.close()
