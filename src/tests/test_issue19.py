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

from tests import copyTestFile


class FLACRemoveTagsTest(unittest.TestCase):
    """A test for removing existing tags in FLAC.

    Motivated by https://github.com/supermihi/pytaglib/issues/19.
    """

    def test_set_to_empty_string(self):
        with copyTestFile('issue19.flac') as copy_file:
            tfile = taglib.File(copy_file)
            tfile.tags['COMMENT'] = ['']
            tfile.save()
            tfile.close()

            tfile = taglib.File(copy_file)
            self.assertNotIn('COMMENT', tfile.tags)
            tfile.close()

    def test_set_to_empty_list(self):
        with copyTestFile('issue19.flac') as copy_file:
            tfile = taglib.File(copy_file)
            tfile.tags['COMMENT'] = []
            tfile.save()
            tfile.close()

            tfile = taglib.File(copy_file)
            self.assertNotIn('COMMENT', tfile.tags)
            tfile.close()

    def test_delete_key(self):
        with copyTestFile('issue19.flac') as copy_file:
            tfile = taglib.File(copy_file)
            del tfile.tags['COMMENT']
            tfile.save()
            tfile.close()

            tfile = taglib.File(copy_file)
            self.assertNotIn('COMMENT', tfile.tags)
            tfile.close()

    def test_set_to_space(self):
        with copyTestFile('issue19.flac') as copy_file:
            tfile = taglib.File(copy_file)
            tfile.tags['COMMENT'] = [' ']
            tfile.save()
            tfile.close()

            tfile = taglib.File(copy_file)
            self.assertIn('COMMENT', tfile.tags)
            self.assertEqual(tfile.tags['COMMENT'][0], ' ')
            tfile.close()


if __name__ == '__main__':
    unittest.main()
