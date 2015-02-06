pytaglib – TagLib bindings for Python 2.x/3.x
==============================================

Overview
--------

pytaglib is a package of Python_ (2.6+/3.1+) bindings for Taglib_. To my
knowledge this so far is the only full-featured audio metadata library that
supports Python 3.x.

Also, the package gives you complete freedom over the tag names – you are
not limited to common tags like ``ARTIST``, ``ALBUM`` etc.; instead you may use
any string as key as long as the underlying metadata format supports it (most
of them do, including mp3, ogg, and FLAC). Moreover, you can even use multiple
values of the same tag, to e.g. store two artists, several genres, and so on.
 
.. _Python: http://www.python.org
.. _Taglib: http://taglib.github.com


Requirements
------------

Pytaglib uses Taglib_ features that have been added only in version 1.8-BETA,
so you need at least that version along with development headers. The recent
releases of most linux flavours nowadays ship taglib-1.8, including:

- Ubuntu 12.10
- Debian jessie (currently testing) or wheezy-packports
- Linux Mint 14
- Up-to-date Arch Linux
- Up-to-date Gentoo Linux
- Fedora 17

The use of taglib >= 1.9 is recommended, since that release fixes some bugs
that may affect pytaglib in less common circumstances.
 
Installation
------------

Debian sid and Ubuntu trusty have binary packages for the python3 version, called python3-taglib.
For Arch users, there is a `package <https://aur.archlinux.org/packages/python-pytaglib/>`_ in the
user repository (AUR).

If your distribution does not ship pytaglib, it can easily be installed by one of the following
methods.

- The easiest way is to use pip or easy_install:

        sudo pip install pytaglib

    or

        sudo easy_install pytaglib

    On systems which use Python 2 by default, this will compile and instal the Python 2 version.
    Use something like

        sudo easy_install3 pytaglib

    to build the package for Python 3 (the exact command depends on your
    distribution). Both commands can be run with the ``--user`` option (and without ``sudo``) which will
    install everything into your home directory.

- Alternatively, you can download the source tarball and compile manually:

        python3 setup.py build
        python3 setup.py test  # optional
        sudo python3 setup.py install

    Replace ``python3`` by the interpreter executable of the desired Python version.

The compiler must be able to find headers and dynamic library of TagLib_. Usually, they should be
installed at standard places. If not, you can manually specify include and lib directories, e.g.:

    python setup.py build_ext --include-dirs /usr/local/include --library-dirs /usr/local/lib

The ``taglib`` Python extension is built from the file ``taglib.cpp`` which is, in turn,
auto-generated with `Cython <www.cython.org>`_ from ``taglib.pyx``. To re-cythonize this file
instead of using the shipped ``taglib.cpp``, invoke ``setup.py`` with the ``--cython`` option.


Basic Usage
-----------

The use of the library is pretty straightforward:

1.  Load the library: ``import taglib``
2.  Open a file: ``f = taglib.File("/path/to/file.mp3")``
3.  Read tags from the dict ``f.tags``, mapping uppercase tag names to lists
    of tag values (note that even single values are stored as list in order
    to be consistent).
4.  Some other information about the file is available as well: ``f.length``,
    ``f.sampleRate``, ``f.channels``, ``f.bitrate``, and ``f.readOnly``.
5.  Alter the tags by manipulating the dictionary ``f.tags``. You should always
    use uppercase tag names and the values must be strings.
6.  Save everything: ``retval = f.save()``.
7.  If some tags could not be saved because they are not supported by the
    underlying format, those will be contained in the value returned from
    ``f.save()``.
 
The following snippet should show the most relevant features. For a complete
reference confer the online help via ``help(taglib.File)``.

::

    $ python
    Python 3.3.0 (default, Sep 29 2012, 15:50:43)
    [GCC 4.7.1 20120721 (prerelease)] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import taglib
    >>> f = taglib.File("x.flac")
    >>> f
    File('x.flac')
    >>> f.tags
    {'ARTIST': ['piman', 'jzig'], 'ALBUM': ['Quod Libet Test Data'], 'TITLE': ['Silence'], 'GENRE': ['Silence'], 'TRACKNUMBER': ['02/10'], 'DATE': ['2004']}
    >>> f.tags["ALBUM"] = ["Always use lists even for single values"]
    >>> del f.tags["GENRE"]
    >>> f.tags["ARTIST"].remove("jzig")
    >>> retval = f.save()
    >>> retval
    {}
    >>>

pyprinttags
-----------

This package also installs the small script ``pyprinttags``. It takes one or more files as
command-line parameters and will display all known metadata of that files on the terminal.
If unsupported tags (a.k.a. non-textual information) are found, they can optionally be removed
from the file.
