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


def test_cyrillic_file_name(tmpdir):
    """Motivated by https://github.com/supermihi/pytaglib/issues/28.
    """
    copy_file = copy_test_file('Жбж.mp3', tmpdir)
    tfile = taglib.File(copy_file)
    tfile.tags['COMMENT'] = ['test']
    tfile.save()
    tfile.close()
