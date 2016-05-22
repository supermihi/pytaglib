# -*- coding: utf-8 -*-
# Copyright 2011-2016 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
from __future__ import unicode_literals
import unittest
import taglib
from . import copyTestFile


class TestStringValue(unittest.TestCase):

    def test_strval(self):
        """Ensure writing single tag values instead of lists is supported (using both bytes and
        unicode)."""
        with copyTestFile('testöü.flac') as f:
            tf = taglib.File(f)
            tf.tags['AAA'] = u'A TAG'
            tf.tags['BBB'] = b'ANOTHER TAG'
            tf.save()
            del tf
            tf = taglib.File(f)
            self.assertEqual(tf.tags['AAA'], ['A TAG'])
            self.assertEqual(tf.tags['BBB'], ['ANOTHER TAG'])
            tf.close()
