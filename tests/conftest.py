# -*- coding: utf-8 -*-
# Copyright 2019 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#

import shutil
from pathlib import Path

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


# A minimal valid 1x1 red PNG image (67 bytes)
TINY_PNG = bytes([
    0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D,
    0x49, 0x48, 0x44, 0x52, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
    0x08, 0x02, 0x00, 0x00, 0x00, 0x90, 0x77, 0x53, 0xDE, 0x00, 0x00, 0x00,
    0x0C, 0x49, 0x44, 0x41, 0x54, 0x08, 0xD7, 0x63, 0xF8, 0xCF, 0xC0, 0x00,
    0x00, 0x00, 0x03, 0x00, 0x01, 0x00, 0x05, 0xFE, 0xD4, 0xEF, 0x00, 0x00,
    0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82
])


@pytest.fixture(scope='session')
def tiny_png() -> bytes:
    return TINY_PNG
