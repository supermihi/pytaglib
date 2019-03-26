# -*- coding: utf-8 -*-
# Copyright 2011-2016 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#

from __future__ import absolute_import, unicode_literals

import taglib

from . import copy_test_file


def test_flac_supports_unicode_value(tmpdir):
    copy_file = copy_test_file('testöü.flac', tmpdir)
    tfile = taglib.File(copy_file)
    tfile.tags['ARTIST'] = ['artøst 1', 'artöst 2']
    tfile.save()
    tfile.close()

    tfile = taglib.File(copy_file)
    assert tfile.tags['ARTIST'] == ['artøst 1', 'artöst 2']
    tfile.close()


def test_flac_supports_unicode_key(tmpdir):
    copy_file = copy_test_file('testöü.flac', tmpdir)
    tfile = taglib.File(copy_file)
    tfile.tags['HÄÜ'] = ['omg']
    remaining = tfile.save()
    assert 'HÄÜ' in remaining
    tfile.close()
