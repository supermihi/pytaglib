# -*- coding: utf-8 -*-
# Copyright 2011-2017 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#

import taglib


def test_cyrillic_file_name(test_file):
    """Motivated by https://github.com/supermihi/pytaglib/issues/28."""
    tfile = test_file("Жбж.mp3")
    tfile.tags["COMMENT"] = ["test"]
    tfile.save()
    tfile.close()


def test_accepts_bytes_keys_and_values(test_data):
    f = test_data("rare_frames.mp3")
    tf = taglib.File(f)
    tf.tags[b"BYTES"] = [b"OnE", b"twO"]
    tf.save()
    tf.close()

    tf = taglib.File(f)
    assert tf.tags["BYTES"] == ["OnE", "twO"]
    tf.close()


def test_accepts_unicode_keys_and_tags(test_data):
    f = test_data("rare_frames.mp3")
    tf = taglib.File(f)
    tf.tags["UNICODE"] = ["OnE", "twO"]
    tf.save()
    tf.close()

    tf = taglib.File(f)
    assert tf.tags["UNICODE"] == ["OnE", "twO"]
    tf.close()
