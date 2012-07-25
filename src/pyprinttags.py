#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2011-2012 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
"""A sample script printing the tags of a given audio file.

The main purpose is to show how pytaglib is used, but it also serves as a tool
showing *all* metadata of a given while, while most taggers only display a set
of certain tags they know.
"""

import sys
import taglib

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('need exactly one argument, the path of the file')
    audioFile = taglib.File(sys.argv[1])
    tags = audioFile.tags
    if len(tags) > 0:
        maxKeyLen = max(len(key) for key in tags.keys())
        for key, values in tags.items():
            for value in values:
                print(('{0:' + str(maxKeyLen) + '} = {1}').format(key, value))
    if len(audioFile.unsupported) > 0:
        print('Unsupported tag elements: ' + "; ".join(audioFile.unsupported))
        if input("remove unsupported properties? [yN] ") in "yY":
            audioFile.removeUnsupportedProperties(audioFile.unsupported)
            audioFile.save()