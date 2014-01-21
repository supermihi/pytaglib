# -*- coding: utf-8 -*-
# Copyright 2011-2014 Michael Helmling
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
        """See https://bugs.kde.org/show_bug.cgi?id=298183
        
        Should be fixed in recent taglib versions.
        """
        with copyTestFile('rare_frames.mp3') as f:
            tfile = taglib.File(f, True)
            self.assert_('GENRE' in tfile.tags)
            self.assertEqual(len(tfile.tags['GENRE']), 1)
            del tfile.tags['GENRE']
            tfile.save()
            del tfile
            tfile = taglib.File(f)
            self.assert_('GENRE' not in tfile.tags)
            
    def test_removeFrame2(self):
        """See https://bugs.kde.org/show_bug.cgi?id=298183."""
        with copyTestFile('r2.mp3') as f:
            tfile = taglib.File(f, True)
            self.assert_('TITLE' in tfile.tags)
            self.assertEqual(len(tfile.tags['TITLE']), 1)
            del tfile.tags['TITLE']
            tfile.save()
            del tfile
            tfile = taglib.File(f)
            self.assert_('TITLE' not in tfile.tags)

    def test_id3v1Tov2(self):
        with copyTestFile('onlyv1.mp3') as f:
            tfile = taglib.File(f, True)
            self.assert_('ARTIST' in tfile.tags)
            self.assertEqual(tfile.tags['ARTIST'][0], 'Bla')
            tfile.tags["NONID3V1"] = ["omg", "wtf"]
            ret = tfile.save()
            self.assertEqual(len(ret), 0)
            
            tfile = taglib.File(f)
            self.assert_('NONID3V1' in tfile.tags)
