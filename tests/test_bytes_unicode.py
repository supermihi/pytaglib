# -*- coding: utf-8 -*-
# Copyright 2011-2017 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
from __future__ import unicode_literals

import taglib
from . import copy_test_file



def test_cyrillic_file_name(tmpdir):
    """Motivated by https://github.com/supermihi/pytaglib/issues/28.
    """
    copy_file = copy_test_file('Жбж.mp3', tmpdir)
    tfile = taglib.File(copy_file)
    tfile.tags['COMMENT'] = ['test']
    tfile.save()
    tfile.close()


def test_accepts_bytes_keys_and_values(tmpdir):
    f = copy_test_file('rare_frames.mp3', tmpdir)
    tf = taglib.File(f)
    tf.tags[b'BYTES'] = [b'OnE', b'twO']
    tf.save()
    tf.close()

    tf = taglib.File(f)
    assert tf.tags['BYTES'] == ['OnE', 'twO']
    tf.close()


def test_accepts_unicode_keys_and_tags(tmpdir):
    f = copy_test_file('rare_frames.mp3', tmpdir)
    tf = taglib.File(f)
    tf.tags[u'UNICODE'] = [u'OnE', u'twO']
    tf.save()
    tf.close()

    tf = taglib.File(f)
    assert tf.tags['UNICODE'] == ['OnE', 'twO']
    tf.close()
