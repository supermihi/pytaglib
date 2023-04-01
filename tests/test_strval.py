# -*- coding: utf-8 -*-
# Copyright 2011-2016 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
import taglib


def test_string_value_is_converted_to_list(test_data):
    f = test_data("testöü.flac")
    tf = taglib.File(f)
    tf.tags["AAA"] = "A TAG"
    tf.tags["BBB"] = b"ANOTHER TAG"
    tf.save()
    tf.close()
    del tf
    tf = taglib.File(f)
    assert tf.tags["AAA"] == ["A TAG"]
    assert tf.tags["BBB"] == ["ANOTHER TAG"]
    tf.close()
