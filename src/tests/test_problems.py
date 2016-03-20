# -*- coding: utf-8 -*-
# Copyright 2011-2015 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
from __future__ import unicode_literals
import unittest, os, stat
import taglib
from . import copyTestFile


class TestProblems(unittest.TestCase):
    """Test for various "problem" cases: non-existent files, readonly files, ... more to come"""
    
    def test_fileNotExist(self):
        """Ensure OSError is raised if a file does not exist, or is a directory."""
        self.assertRaises(OSError, taglib.File, '/this/file/almost/certainly/does/not/exist.flac')
        self.assertRaises(OSError, taglib.File, '/spæciäl/chàracterß.mp3')
        self.assertRaises(OSError, taglib.File, '/usr')
        self.assertRaises(OSError, taglib.File, "/nonexistent.ogg") # segfaults due to taglib bug
        
    def test_readOnly(self):
        """Ensure OSError is raised when save() is called on read-only files."""
        with copyTestFile('rare_frames.mp3') as f:
            os.chmod(f, stat.S_IREAD)
            tf = taglib.File(f)
            self.assertTrue(tf.readOnly)
            self.assertRaises(OSError, tf.save)
            os.chmod(f, stat.S_IREAD & stat.S_IWRITE)
            tf.close()
