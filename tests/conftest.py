# -*- coding: utf-8 -*-
# Copyright 2019 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#

from pathlib import Path
import shutil

import pytest
import taglib


@pytest.fixture
def test_data(tmp_path):
    def result(filename):
        """Make a temporary copy of test data file *name* (without dir) and return its full path."""
        source = Path(__file__).parent / "data" / filename
        target = tmp_path / filename
        shutil.copyfile(source, target)
        return target

    return result


@pytest.fixture
def test_file(test_data):
    def result(filename):
        data_file = test_data(filename)
        return taglib.File(data_file)

    return result
