# -*- coding: utf-8 -*-
# Copyright 2011-2017 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#

from __future__ import absolute_import, unicode_literals

import taglib

from tests import copy_test_file

"""Tests for removing existing tags in FLAC.

Motivated by https://github.com/supermihi/pytaglib/issues/19.
"""


def test_set_value_to_empty_string_removes_tag(tmpdir):
    copy_file = copy_test_file('issue19.flac', tmpdir)
    tfile = taglib.File(copy_file)
    tfile.tags['COMMENT'] = ['']
    tfile.save()
    tfile.close()

    tfile = taglib.File(copy_file)
    assert 'COMMENT' not in tfile.tags
    tfile.close()


def test_set_value_to_empty_list_removes_tag(tmpdir):
    copy_file = copy_test_file('issue19.flac', tmpdir)
    tfile = taglib.File(copy_file)
    tfile.tags['COMMENT'] = []
    tfile.save()
    tfile.close()

    tfile = taglib.File(copy_file)
    assert 'COMMENT' not in tfile.tags
    tfile.close()


def test_delete_key_removes_tag(tmpdir):
    copy_file = copy_test_file('issue19.flac', tmpdir)
    tfile = taglib.File(copy_file)
    del tfile.tags['COMMENT']
    tfile.save()
    tfile.close()

    tfile = taglib.File(copy_file)
    assert 'COMMENT' not in tfile.tags
    tfile.close()


def test_set_value_to_space_does_not_remove_tag(tmpdir):
    copy_file = copy_test_file('issue19.flac', tmpdir)
    tfile = taglib.File(copy_file)
    tfile.tags['COMMENT'] = [' ']
    tfile.save()
    tfile.close()

    tfile = taglib.File(copy_file)
    assert 'COMMENT' in tfile.tags
    assert tfile.tags['COMMENT'][0] == ' '
    tfile.close()
