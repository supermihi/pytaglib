# -*- coding: utf-8 -*-
# Copyright 2011-2016 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
from __future__ import absolute_import, unicode_literals

import taglib
import unittest
import os
import stat

from tests import copyTestFile


class TestCyrillicFileName(unittest.TestCase):
    """Motivated by https://github.com/supermihi/pytaglib/issues/28.
    """

    def test_issue28(self):
        with copyTestFile('Жбж.mp3') as copy_file:
            tfile = taglib.File(copy_file)
            tfile.tags['COMMENT'] = ['test']
            tfile.save()
            tfile.close()
