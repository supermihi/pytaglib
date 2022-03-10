# **pytaglib**
[![PyPI](https://img.shields.io/pypi/v/pytaglib.svg)](https://pypi.org/project/pytaglib/)

pytaglib is a [Python](https://www.python.org) audio tagging library. It is cross-platform and very simple to use yet fully featured:
 - [supports more than a dozen file formats](https://taglib.org/) including mp3, flac, ogg, wma, and mp4,
 - support arbitrary, non-standard tag names,
 - support multiple values per tag.

pytaglib is a very thin wrapper (≈150 lines of [code](src/taglib.pyx)) around the fast and rock-solid [TagLib](https://taglib.org/) C++ library.
## News
See the [Changelog](CHANGELOG.md).
## Get it
At first, you might need to install taglib with development headers. Ubuntu, Mint and other Debian-Based distributions:
        
        sudo apt install libtag1-dev

On a Mac, use HomeBrew:
        
        brew install taglib

Then install pytaglib with [pip](https://pip.pypa.io/en/stable/):

        pip install pytaglib


        
For other operating systems and more details, see [installation notes](#installation-notes) below.

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

* Ensure that `pip` is installed and points to the correct Python version
  - on Windows, be sure to check *install pip* in the Python installer
  - on Debian/Ubuntu/Mint, install `python3-pip`
  - you might need to type, e.g., `pip-3` to install pytaglib for Python 3 if your system's default is Python 2.x.
* For Windows users, there are some precompiled binary packages (wheels). See the [PyPI page](https://pypi.python.org/pypi/pytaglib) for a list of supported Python versions.
* If no binary packages exists, you need to have both Python and taglib installed with development headers (packages `python3-dev` (or `python-dev`) and `libtag1-dev` for debian / ubuntu and derivates, `python-devel` and `taglib-devel` for fedora and friends, `brew install taglib` on OS X).


### Linux: Distribution-Specific Packages
* Debian- and Ubuntu-based linux flavors have binary packages for the Python 3 version, called `python3-taglib`. Unfortunatelly, they are heavily outdated, so you should instally the recent version via `pip` whenever possible.
* For Arch users, there is a [package](https://aur.archlinux.org/packages/python-pytaglib/) in the user repository (AUR).

### Manual Compilation: General
You can download or checkout the sources and compile manually:

        pip install .
        # if you want to run the unit tests, use these commands instead
        # pip install .[tests]
        # python -m pytest

### Compilation: Windows

Install MS Visual Studio Build Tools (or the complete IE) and include the correct compiler version as detailed [here](https://wiki.python.org/moin/WindowsCompilers). Also enable *cmake* in the Visual Studio Installer.

Then:
- open the VS native tools command prompt
- navigate to the *pytaglib* repository
- run `python build_taglib_windows.py` which will download and build the latest official TagLib release
- run `python setup.py install`


## Contact
For bug reports or feature requests, please use the
[issue tracker](https://github.com/supermihi/pytaglib/issues) on GitHub. For anything else, contact
me by [email](mailto:michaelhelmling@posteo.de).
