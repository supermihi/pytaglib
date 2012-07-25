pytaglib -- TagLib bindings for Python 2.x/3.x
==============================================

Overview
--------

pytaglib is a package of Python_ (2.x/3.x) bindings for TagLib_. To my
knowledge this so far is the only full-featured audio metadata library that
supports python3.x.

Also, the package gives you complete freedom over the tag names -- you are
not limited to common tags like 'ARTIST', 'ALBUM' etc.; instead you may use
any string as key as long as the underlying metadata format supports it (most
of them do, including MP3, OGG, and FLAC). Moreover, you can even use multiple
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
so you need at least that version along with development headers.

..  _Cython: http://www.cython.org
  
Installation
------------
::
	python3 setup.py build
	python3 setup.py test  # optional
	sudo python3 setup.py install

Replace ``3`` by whatever Python version you use.

Usage
-----
::
	$ python3
	Python 3.2.2rc1 (default, Aug 14 2011, 19:02:04) 
	[GCC 4.6.1] on linux2
	Type "help", "copyright", "credits" or "license" for more information.
	>>> import taglib
	>>> f = taglib.File("x.ogg")
	>>> f.tags
	{'ALBUM': ['omgwtf', 'lol'], 'ARTIST': ['öätrnüö']}
	>>> f.length
	472
	>>> f.sampleRate
	44100
	>>> f.tags["ARTIST"] = ["A new artist"]
	>>> del f.tags['ALBUM']
	>>> 
	>>> f.save()
	True
	>>>
