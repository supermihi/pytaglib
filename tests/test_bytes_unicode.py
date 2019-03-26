# -*- coding: utf-8 -*-
# Copyright 2011-2017 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
from __future__ import unicode_literals
import sys
import taglib
from . import copy_test_file


def test_bytes_filename(tmpdir):
    """Ensure file can be opened if filename is provided as bytes object."""
    f = copy_test_file('testöü.flac', tmpdir)
    tf = taglib.File(f.encode('utf8'))
    tf.close()


def test_unicode_filename(tmpdir):
    """Ensure file can be opened if filename is provided as bytes object."""
    f = copy_test_file('testöü.flac', tmpdir)
    if sys.version_info.major == 2:
        f = unicode(f)
    tf = taglib.File(f)
    tf.close()


def test_bytes_tags(tmpdir):
    """Ensure bytes keys and values are accepted.

    Update 2017-05-12: Use mixed-case tag values as a regression test for issue #33.
    """
    f = copy_test_file('rare_frames.mp3', tmpdir)
    tf = taglib.File(f)
    tf.tags[b'BYTES'] = [b'OnE', b'twO']
    tf.save()
    tf.close()

    tf = taglib.File(f)
    assert tf.tags['BYTES'] == ['OnE', 'twO']
    tf.close()


def test_unicode_tags(tmpdir):
    """Ensure unicode keys and values are accepted."""
    f = copy_test_file('rare_frames.mp3', tmpdir)
    tf = taglib.File(f)
    tf.tags[u'UNICODE'] = [u'OnE', u'twO']
    tf.save()
    tf.close()

    tf = taglib.File(f)
    assert tf.tags['UNICODE'] == ['OnE', 'twO']
    tf.close()
