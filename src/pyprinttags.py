#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2011-2012 Michael Helmling
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
    file = taglib.File(sys.argv[1])
    tags = file.tags
    if len(tags) > 0:
        maxKeyLen = max(map(len, tags.keys()))
        for key, values in tags.items():
            for value in values:
                print(('{0:' + str(maxKeyLen) + '} = {1}').format(key, value))
    if len(file.unsupported) > 0:
        print('Unsupported tag elements: ' + "; ".join(file.unsupported))
        if input("remove unsupported properties? [yN] ") in "yY":
            file.removeUnsupportedProperties(file.unsupported)
            file.save()