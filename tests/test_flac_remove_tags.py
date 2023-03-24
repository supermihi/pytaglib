# -*- coding: utf-8 -*-
# Copyright 2011-2017 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
import taglib

"""Tests for removing existing tags in FLAC.

Motivated by https://github.com/supermihi/pytaglib/issues/19.
"""


def test_set_value_to_empty_string_removes_tag(test_data):
    file = test_data("issue19.flac")
    tfile = taglib.File(file)
    tfile.tags["COMMENT"] = [""]
    tfile.save()
    tfile.close()

    tfile = taglib.File(file)
    assert "COMMENT" not in tfile.tags
    tfile.close()


def test_set_value_to_empty_list_removes_tag(test_data):
    file = test_data("issue19.flac")
    tfile = taglib.File(file)
    tfile.tags["COMMENT"] = []
    tfile.save()
    tfile.close()

    tfile = taglib.File(file)
    assert "COMMENT" not in tfile.tags
    tfile.close()


def test_delete_key_removes_tag(test_data):
    file = test_data("issue19.flac")
    tfile = taglib.File(file)
    del tfile.tags["COMMENT"]
    tfile.save()
    tfile.close()

    tfile = taglib.File(file)
    assert "COMMENT" not in tfile.tags
    tfile.close()


def test_set_value_to_space_does_not_remove_tag(test_data):
    file = test_data("issue19.flac")
    tfile = taglib.File(file)
    tfile.tags["COMMENT"] = [" "]
    tfile.save()
    tfile.close()

    tfile = taglib.File(file)
    assert "COMMENT" in tfile.tags
    assert tfile.tags["COMMENT"][0] == " "
    tfile.close()
