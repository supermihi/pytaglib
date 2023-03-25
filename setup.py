#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2019 Michael Helmling, michaelhelmling@posteo.de
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
"""Setup file for pytaglib. Type <python setup.py install> to install this package."""

import os
import platform
import re
import sys
from pathlib import Path

from Cython.Build import cythonize
from setuptools import setup, Extension

is_x64 = sys.maxsize > 2**32
arch = "x64" if is_x64 else "x32"
system = platform.system()
python_version = platform.python_version()
here = Path(__file__).resolve().parent
default_taglib_path = here / "build" / "taglib" / f"{system}-{arch}-py{python_version}"

CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Cython",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

src = Path("src")


def readme():
    readme_file = here / "README.md"
    return readme_file.read_text("utf-8")


def extension_kwargs():
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
        )


def version():
    taglib_pyx = here / src / "taglib.pyx"
    version_match = re.search(
        r"^version = ['\"]([^'\"]*)['\"]", taglib_pyx.read_text(), re.M
    )
    return version_match.group(1)


setup(
    name="pytaglib",
    description='cross-platform, Python audio metadata ("tagging") library based on TagLib',
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=CLASSIFIERS,
    version=version(),
    license="GPLv3+",
    author="Michael Helmling",
    author_email="michaelhelmling@posteo.de",
    url="http://github.com/supermihi/pytaglib",
    ext_modules=cythonize(
        [Extension("taglib", [str(src / "taglib.pyx")], **extension_kwargs())],
        force=True,
    ),
    package_dir={"": "src"},
    py_modules=["pytaglib", "pyprinttags"],
    entry_points={"console_scripts": ["pyprinttags=pyprinttags:script"]},
    extras_require={
        "tests": ["pytest"],
    },
    python_requires=">=3.6",
)
