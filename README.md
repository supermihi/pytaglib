# **pytaglib**

[![PyPI](https://img.shields.io/pypi/v/pytaglib.svg)](https://pypi.org/project/pytaglib/)

pytaglib is a [Python](https://www.python.org) audio tagging library. It is cross-platform and very simple to use yet fully featured:

- [supports more than a dozen file formats](https://taglib.org/) including mp3, flac, ogg, wma, and mp4,
- support arbitrary, non-standard tag names,
- support multiple values per tag.

pytaglib is a very thin wrapper around the fast and rock-solid [TagLib](https://taglib.org/) C++ library.

## News

_2025-11-17_ pytaglib-3.1.0 has been released.

- build wheels for recent Python versions (up to 3.14)
- build wheels for PyPy again
- bump bundled taglib (in wheels) to v2.1.1

For a full list of changes in this and previous releases, see the [Changelog](CHANGELOG.md).

## Install

Use your favorite Python package manager to install the `pytaglib` package. Example when using [pip](https://pip.pypa.io/en/stable/):

        pip install pytaglib

In most cases, this should pick a provided binary wheel that bundles the native TagLib library suitable for your platform. If it doesn't, and the
installation fails, see [below](#installation-notes).

## Usage

```python
>>> import taglib
>>> with taglib.File("/path/to/my/file.mp3", save_on_exit=True) as song:
>>>     song.tags
{'ARTIST': ['piman', 'jzig'], 'ALBUM': ['Quod Libet Test Data'], 'TITLE': ['Silence'], 'GENRE': ['Silence'], 'TRACKNUMBER': ['02/10'], 'DATE': ['2004']}

>>>     song.length
239
>>>     song.tags["ALBUM"] = ["White Album"] # always use lists, even for single values
>>>     del song.tags["DATE"]
>>>     song.tags["GENRE"] = ["Vocal", "Classical"]
>>>     song.tags["PERFORMER:HARPSICHORD"] = ["Ton Koopman"]
>>> # with save_on_exit=True, file will be saved at the end of the 'with' block
```

For detailed API documentation, use the docstrings of the `taglib.File` class or view the [source code](src/taglib.pyx) directly.

## `pyprinttags`

This package also installs the `pyprinttags` script. It takes one or more files as
command-line parameters and will display all known metadata of that files on the terminal.
If unsupported tags (a.k.a. non-textual information) are found, they can optionally be removed
from the file.

## Installation Notes

Things are a bit more complicated than usual with Python because pytaglib requires the native (C++) TagLib library.

If there are no binary wheels for your platform, or you want to manually
compile pytaglib, you will need to have Taglib installed with development headers,
and also development tools for Python.

On Ubuntu, Mint and other Debian-Based distributions, install
the `libtag1-dev` and `python-dev` packages. On Fedora and friends, these are called `taglib-devel` and `python-devel`, respectively. On a Mac, use HomeBrew to install the `taglib` package. For Windows, see below.

As an alternative, run `python build_native_taglib.py` in this directory to
automatically download and build the latest Taglib version into the `lib/taglib-cpp` subdirectory (also works on
Windows).

This requires Python and a suitable compiler to be installed; specific instructions are beyond the
scope of this README.

### Linux: Distribution-Specific Packages

- Debian- and Ubuntu-based linux flavors have binary packages for the Python 3 version, called `python3-taglib`. Unfortunatelly, they are heavily outdated, so you should instally the recent version via `pip` whenever possible.
- For Arch users, there is a [package](https://aur.archlinux.org/packages/python-pytaglib/) in the user repository (AUR).

### Manual Compilation: General

To create a binary wheel for your platform, use any PEP-517 compatible build frontend. Example using [build](https://github.com/pypa/build):

        python -m build

or with uv:

        uv build

which will place the wheel inside the `dist` directory.

### Compilation: Windows

Install MS Visual Studio Build Tools (or the complete IE) and include the correct compiler version as detailed [here](https://wiki.python.org/moin/WindowsCompilers). Also enable _cmake_ in the Visual Studio Installer.

Then:

- open the VS native tools command prompt
- navigate to the _pytaglib_ repository
- run `python build_native_taglib.py` which will download and build the latest official TagLib release
- run `python setup.py install`

## Development

To start hacking (contributions welcome!), clone the repository and set up a project environment with your favorite tool. I use [uv](https://docs.astral.sh/uv/), where you should need only two commands for most workflows:

    # set up virtual environment, run cythonize, compile
    $ uv sync --reinstall

    # run tests
    $ uv run pytest
## Contact

For bug reports or feature requests, please use the
[issue tracker](https://github.com/supermihi/pytaglib/issues) on GitHub. For anything else, contact
me by [email](mailto:michaelhelmling@posteo.de).
