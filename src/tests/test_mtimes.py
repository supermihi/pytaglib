# -*- coding: utf-8 -*-
# Copyright 2011-2015 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#

from __future__ import absolute_import, unicode_literals
import unittest, taglib
import os
import time
from . import copyTestFile
from decimal import Decimal as D


class FLACUnicodeTest(unittest.TestCase):
    """A test for unicode tags in FLAC"""

    def test_default_mtime(self):
        with copyTestFile('testöü.flac') as copy_file:
            stats0 = os.stat(copy_file)
            mtime0 = D.from_float(stats0.st_mtime)

            tfile = taglib.File(copy_file)
            tfile.tags['TAG'] = ['mtime test']
            time.sleep(.01)
            tfile.save()

            stats = os.stat(copy_file)
            mtime = D.from_float(stats.st_mtime)

            self.assertNotEqual(mtime0, mtime)

    def test_preserved_mtime(self):
        with copyTestFile('testöü.flac') as copy_file:
            stats0 = os.stat(copy_file)
            mtime0 = stats0.st_mtime

            tfile = taglib.File(copy_file)
            tfile.tags['TAG'] = ['mtime test']
            time.sleep(.01)
            tfile.save(preserve_mtime=True)

            stats = os.stat(copy_file)
            mtime = stats.st_mtime

            self.assertEqual(mtime0, mtime)

if __name__ == '__main__':
    unittest.main()

