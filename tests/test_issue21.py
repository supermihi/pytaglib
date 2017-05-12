# -*- coding: utf-8 -*-
# Copyright 2011-2017 Michael Helmling
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


class TestReadOnlyErrorNonAscii(unittest.TestCase):
    """Motivated by https://github.com/supermihi/pytaglib/issues/21.
    """

    def test_issue21(self):
        with copyTestFile('readönly.mp3') as copy_file:
            os.chmod(copy_file, stat.S_IREAD)
            tfile = taglib.File(copy_file.encode('utf8'))
            tfile.tags['COMMENT'] = ['']
            self.assertRaises(OSError, tfile.save)
            tfile.close()
