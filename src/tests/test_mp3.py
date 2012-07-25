# -*- coding: utf-8 -*-
# Copyright 2011-2012 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
from __future__ import unicode_literals
import unittest, taglib
from . import copyTestFile

class ID3v2Test(unittest.TestCase):
    
    def test_removeFrame1(self):
        """See https://bugs.kde.org/show_bug.cgi?id=298183"""
        with copyTestFile('rare_frames.mp3') as f:
            tfile = taglib.File(f)
            self.assertIn('GENRE', tfile.tags)
            self.assertEqual(len(tfile.tags['GENRE']), 1)
            del tfile.tags['GENRE']
            tfile.save()
            del tfile
            tfile = taglib.File(f)
            self.assertNotIn('GENRE', tfile.tags)
            
    def test_removeFrame2(self):
        """See https://bugs.kde.org/show_bug.cgi?id=298183"""
        with copyTestFile('id3v22-tda.mp3') as f:
            tfile = taglib.File(f)
            self.assertIn('TITLE', tfile.tags)
            self.assertEqual(len(tfile.tags['TITLE']), 1)
            del tfile.tags['TITLE']
            tfile.save()
            del tfile
            tfile = taglib.File(f)
            self.assertNotIn('TITLE', tfile.tags)