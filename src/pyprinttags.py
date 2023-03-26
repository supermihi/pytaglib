#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Michael Helmling, michaelhelmling@posteo.de
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
import argparse
import sys

import taglib


def script():
    """Print tags of given files"""
    parser = argparse.ArgumentParser(
        description="Print all textual tags of one or more audio files."
    )
    parser.add_argument("file", nargs="+", help="file(s) to print tags of")
    args = parser.parse_args()
    for i, filename in enumerate(args.file):
        print(f"{filename}:")
        file = taglib.File(filename)
        tags = file.tags
        if len(tags) > 0:
            max_key_len = max(len(key) for key in tags.keys())
            for key, values in tags.items():
                for value in values:
                    print(f"  {key.ljust(max_key_len)} = {value}")
        if i < len(args.file) - 1:
            print()


if __name__ == "__main__":
    script()
