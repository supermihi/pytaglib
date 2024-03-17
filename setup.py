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
    taglib_install_dir = Path(os.environ.get("TAGLIB_HOME", str(default_taglib_path)))
    if sys.platform.startswith("win"):
        # on Windows, we compile static taglib build into the python module
        taglib_lib = taglib_install_dir / "lib" / "tag.lib"
        if not taglib_lib.exists():
            raise FileNotFoundError(f"{taglib_lib} not found")
        return dict(
            define_macros=[("TAGLIB_STATIC", None)],
            extra_objects=[str(taglib_lib)],
            include_dirs=[str(taglib_install_dir / "include")],
        )
    else:
        # On unix systems, use the dynamic library. Still, add the (default) TAGLIB_HOME
        # to allow overriding system taglib with custom build.
        return dict(
            libraries=["tag"],
            include_dirs=[str(taglib_install_dir / "include")],
            library_dirs=[
                str(taglib_install_dir / "lib"),
                str(taglib_install_dir / "lib64"),
            ],
            extra_compile_args=["-std=c++17"],
            extra_link_args=["-std=c++17"],
        )


setup(
    ext_modules=cythonize(
        [Extension("taglib", [str(src / "taglib.pyx")], **extension_kwargs())],
        force=True,
    )
)
