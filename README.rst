pytaglib – TagLib bindings for Python 2.x/3.x
==============================================

Overview
--------

pytaglib is a package of Python_ (2.x/3.x) bindings for TagLib_. To my
knowledge this so far is the only full-featured audio metadata library that
supports python3.x.

Also, the package gives you complete freedom over the tag names – you are
not limited to common tags like ``ARTIST``, ``ALBUM`` etc.; instead you may use
any string as key as long as the underlying metadata format supports it (most
of them do, including mp3, ogg, and FLAC). Moreover, you can even use multiple
values of the same tag, to e.g. store two artists, several genres, and so on.
 
.. _Python: http://www.python.org
.. _Taglib:  http://taglib.github.com


Requirements
------------

To compile the bindings you need need the Cython_ compiler for your version
of python. Note that some distributions do not yet ship Cython compiled for
python3, but you can easily get it by typing:: 

	sudo easy_install3 cython

into a console.

pytaglib uses TagLib_ features that have been added only in version 1.8-BETA,
so you need at least that version along with development headers. The recent
releases of most linux flavours nowadays ship taglib-1.8, including:

- Ubuntu 12.10
- Debian "experimental" branch
- Linux Mint 14
- Up-To-Date Arch Linux
- Gentoo Linux (unstable)
- Fedora 17

The upcoming release 1.9 of taglib is recommended, since it fixes some bugs
that may affect pytaglib in less common circumstances.

..  _Cython: http://www.cython.org
  
Installation
------------

As long as pytaglib is not contained in the major distribution's package
repositories, you have to install it manually by one of the following methods.

The easiest way is to use easy_install::

    sudo easy_install -U pytaglib

On most systems, this will install the python2 version; use something like::

    sudo easy_install3 -U pytaglib

to build the package for python3 (the exact command depends on your
distribution).

Alternatively, you can download the source tarball and compile manually:

::

	python3 setup.py build
	python3 setup.py test  # optional
	sudo python3 setup.py install

Replace ``3`` by whatever Python version you use.

Basic Usage
-----------

The use of the library is pretty straightforward:

#.  Load the library: ``import taglib``
#.  Open a file: ``f = taglib.File("/path/to/file.mp3")``
#.  Read tags from the dict ``f.tags``, mapping uppercase tag names to lists
    of tag values (note that even single values are stored as list in order
    to be consistent).
#.  Some other information about the file is available as well: ``f.length``,
    ``f.sampleRate``, ``f.channels``, ``f.bitrate``, and ``f.readOnly``.
#.  Alter the tags by manipulating the dictionary ``f.tags``. You should always
    use uppercase tag names and the values must be strings.
#.  Save everything: ``retval = f.save()``.
#.  If some tags could not be saved because they are not supported by the
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

This package also installs the small script ``pyprinttags``. It takes a file as
its single command-line parameter and will display all known metadata of that
file on the terminal.
