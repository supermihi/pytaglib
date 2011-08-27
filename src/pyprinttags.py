#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2011 Michael Helmlnig
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#

import sys
import taglib
if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('need exactly one argument, the path of the file')
    tags = taglib.File(sys.argv[1]).tags
    if len(tags) > 0:
        maxKeyLen = max(map(len, tags.keys()))
        for key, values in tags.items():
            for value in values:
                print(('{0:' + str(maxKeyLen) + '} = {1}').format(key, value))