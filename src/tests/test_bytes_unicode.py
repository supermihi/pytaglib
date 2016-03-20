# -*- coding: utf-8 -*-
# Copyright 2011-2015 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
from __future__ import unicode_literals
import unittest, sys
import taglib
from . import copyTestFile


class TestBytesUnicode(unittest.TestCase):

    def test_bytes_filename(self):
        """Ensure file can be opened if filename is provided as bytes object."""
        with copyTestFile('testöü.flac') as f:
            tf = taglib.File(f.encode(sys.getfilesystemencoding()))
            tf.close()

    def test_unicode_filename(self):
        """Ensure file can be opened if filename is provided as bytes object."""
        with copyTestFile('testöü.flac') as f:
            if sys.version_info.major == 2:
                f = unicode(f)
            tf = taglib.File(f)
            tf.close()

    def test_bytes_tags(self):
        """Ensure bytes keys and values are accepted."""
        with copyTestFile('rare_frames.mp3') as f:
            tf = taglib.File(f)
            tf.tags[b'BYTES'] = [b'ONE', b'TWO']
            tf.save()
            tf.close()
            
            tf = taglib.File(f)
            self.assertEqual(tf.tags['BYTES'], ['ONE', 'TWO'])
            tf.close()

    def test_unicode_tags(self):
        """Ensure unicode keys and values are accepted."""
        with copyTestFile('rare_frames.mp3') as f:
            tf = taglib.File(f)
            tf.tags[u'UNICODE'] = [u'ONE', u'TWO']
            tf.save()
            tf.close()
            
            tf = taglib.File(f)
            self.assertEqual(tf.tags['UNICODE'], ['ONE', 'TWO'])
            tf.close()

