#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2019 Michael Helmling, michaelhelmling@posteo.de
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#

import os
import sys
from pathlib import Path

from Cython.Build import cythonize
from setuptools import setup, Extension

src = Path("src")


def extension_kwargs():
    here = Path(__file__).resolve().parent
    default_taglib_path = here / "lib" / "taglib-cpp"
    taglib_dir = Path(os.environ.get("TAGLIB_HOME", str(default_taglib_path)))
    result = {
        "include_dirs": [str(taglib_dir / "include"), str(src)],
        "libraries": [],
        "library_dirs": [],
    }
    build_static = taglib_dir.exists()
    if build_static:
        lib_dir = taglib_dir / "lib"
        result["define_macros"] = [("TAGLIB_STATIC", None)]
        if sys.platform.startswith("win"):
            result["libraries"].append("tag")
            result["library_dirs"].append(str(lib_dir))
        else:
            result["extra_objects"] = [str(lib_dir / "libtag.a")]
    else:
        # fall back to dynamic linking at standard locations
        result["libraries"] = ["tag"]
        result["library_dirs"] = [
            str(taglib_dir / "lib"),
            str(taglib_dir / "lib64"),
        ]
    if sys.platform.startswith("darwin"):
        result["extra_compile_args"] = ["-std=c++17"]
        result["extra_link_args"] = ["-std=c++17"]
    return result


setup(
    ext_modules=cythonize(
        [
            Extension(
                "taglib",
                [str(src / "taglib.pyx"), str(src / "fileref_factory.cpp")],
                **extension_kwargs(),
            )
        ],
        force=True,
    )
)
