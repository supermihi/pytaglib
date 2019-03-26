# -*- coding: utf-8 -*-
# Copyright 2011-2016 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
from __future__ import unicode_literals
import taglib
from . import copy_test_file


def test_string_value_is_converted_to_list(tmpdir):
    f = copy_test_file('testöü.flac', tmpdir)
    tf = taglib.File(f)
    tf.tags['AAA'] = u'A TAG'
    tf.tags['BBB'] = b'ANOTHER TAG'
    tf.save()
    del tf
    tf = taglib.File(f)
    assert tf.tags['AAA'] == ['A TAG']
    assert tf.tags['BBB'] == ['ANOTHER TAG']
    tf.close()
