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

from tests import copy_test_file


class TestM4aAlbumArtist(unittest.TestCase):
    """Motivated by https://github.com/supermihi/pytaglib/issues/46.
    """

    def test_issue46(self):
        with copy_test_file('issue46.m4a') as copy_file:
            tfile = taglib.File(copy_file)
            self.assertIn('ALBUMARTIST', tfile.tags)
            self.assertEquals(['Higginbottom, Edward'], tfile.tags['ALBUMARTIST'])
            tfile.close()
