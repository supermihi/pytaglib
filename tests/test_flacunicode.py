# -*- coding: utf-8 -*-
# Copyright 2011-2016 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
import taglib


def test_flac_supports_unicode_value(test_data):
    file = test_data("testöü.flac")
    tfile = taglib.File(file)
    tfile.tags["ARTIST"] = ["artøst 1", "artöst 2"]
    tfile.save()
    tfile.close()

    tfile = taglib.File(file)
    assert tfile.tags["ARTIST"] == ["artøst 1", "artöst 2"]
    tfile.close()


def test_flac_supports_unicode_key(test_file):
    tfile = test_file("testöü.flac")
    tfile.tags["HÄÜ"] = ["omg"]
    remaining = tfile.save()
    assert "HÄÜ" in remaining
    tfile.close()
