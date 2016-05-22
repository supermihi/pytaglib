#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2011-2016 Michael Helmling, michaelhelmling@posteo.de
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
from __future__ import unicode_literals, print_function

import argparse
import os.path
import sys
import taglib


def script():
    """Run the command-line script."""
    parser = argparse.ArgumentParser(description="Print all textual tags of one or more audio files.")
    parser.add_argument("-b", "--batch", help="disable user interaction", action="store_true")
    parser.add_argument("file", nargs="+", help="file(s) to print tags of")
    args = parser.parse_args()
    for filename in args.file:
        if isinstance(filename, bytes):
            filename = filename.decode(sys.getfilesystemencoding())
        line = "TAGS OF '{0}'".format(os.path.basename(filename))
        print("*" * len(line))
        print(line)
        print("*" * len(line))
        audioFile = taglib.File(filename)
        tags = audioFile.tags
        if len(tags) > 0:
            maxKeyLen = max(len(key) for key in tags.keys())
            for key, values in tags.items():
                for value in values:
                    print(('{0:' + str(maxKeyLen) + '} = {1}').format(key, value))
        if len(audioFile.unsupported) > 0:
            print('Unsupported tag elements: ' + "; ".join(audioFile.unsupported))
            if sys.version_info[0] == 2:
                inputFunction = raw_input
            else:
                inputFunction = input
            if not args.batch and inputFunction("remove unsupported properties? [yN] ").lower() in ["y", "yes"]:
                audioFile.removeUnsupportedProperties(audioFile.unsupported)
                audioFile.save()

if __name__ == '__main__':
    script()
