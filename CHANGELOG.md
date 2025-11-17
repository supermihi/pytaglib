# Changelog
# NEXT
- [!183](https://github.com/supermihi/pytaglib/pull/183): re-enable binary wheels for PyPy
- [!180](https://github.com/supermihi/pytaglib/pull/180): remove deprecated Cython IF by implementing custom C++ FileRef factory
- [!181](https://github.com/supermihi/pytaglib/pull/181): no longer build for Mac OS 13
- [!182](https://github.com/supermihi/pytaglib/pull/182): bump bundled taglib to v2.1.1 and bundled utfcpp to 4.0.8
# pytaglib 3.0.1 (2025-03-21)
- [!155](https://github.com/supermihi/pytaglib/pull/155): build wheels for Python 3.13 and MacOS 15

# pytaglib 3.0.0 (2024-03-16)

This is the first release of pytaglib that targets [Taglib 2.0](https://github.com/taglib/taglib/releases/tag/v2.0),
a major upgrade of the underlying C++ Taglib library.

- [!125](https://github.com/supermihi/pytaglib/pull/125): stop building wheels for out-of-support Python versions 3.6 and 3.7
- [!123](https://github.com/supermihi/pytaglib/pull/123): upgrade to Taglib 2.0

  Thanks to [Urs Fleisch](https://github.com/ufleisch) for help
- [#135](https://github.com/supermihi/pytaglib/pull/135): natively build arm64 wheels on macos-14 runner

## pytaglib 2.1.0 (2023-11-17)

- [!118](https://github.com/supermihi/pytaglib/pull/118): update Taglib version for binary wheels to 1.13.1
- [!117](https://github.com/supermihi/pytaglib/pull/117): modernize packaging / tooling
- [!116](https://github.com/supermihi/pytaglib/pull/116): fix Python 3.12 build

## pytaglib 2.0.0 (2023-03-26)

- update Taglib version for binary wheels to 1.13
- improve `build_taglib.py` helper script (now supports all platforms)
- add `taglib_version()` to the `taglib` module
- bundle native Taglib whith binary wheels (even on Unix). This enables to use the latest Taglib version (distributions often ship outdated
  versions) and removes native dependencies.
- use [cibuildwheel](https://cibuildwheel.readthedocs.io) to provide binary wheels for a multitude of platform / Python version combinations
  (fixes #101 #105)
- allow using `File` as a context manager, optionally saving on exit
- new property `File.is_closed`
- fix #94: Accept `os.PathLike` in constructor

### Breaking Changes:

- `File.path` is now a `Path` object

## pytaglib 1.5.0 (2021-12-18)

- fix #93: publish PyPI packages from GitLab workflow
- fix #92: build windows binary wheels from CI
- fix #89: remove Python 2 support
- fix #88: rename pyprinttags3 --> pyprinttags, ignore unsupported tags in the script

## pytaglib 1.4.6 (2020/02/26)

- fix #65: use tox for testing. Request re-cythonizing module with environment variable `PYTAGLIB_CYTHONIZE` instead of argument to `setup.py` now.
- fix #63: python2 tests did not pass
- fix #62: pyprinttags module did not work

## pytaglib 1.4.5 (2019/03/26)

- Fix published taglib.cpp

## pytaglib 1.4.4 (2018/10/27)

- Remove cython dependency from setup.py (thanks to Popkornium18 for reporting)

## pytaglib 1.4.3 (2018/02/25)

- Fix accidental upload of the Windows version to PyPI. Hopefully fixes #42, #43.

## pytaglib 1.4.2 (2018/01/17)

- Fix #31: Don't use precompiled `taglib.cpp` on Windows

## pytaglib 1.4.1 (2017/05/12)

- Fix #33 (no longer uppercase bytestring tag values)

## pytaglib 1.4 (2016/11/26)

- Windows version: fix filenames with non-local codepage characters
- update README (pip options for custom taglib install dir - thanks to qbuchanan)
- build windows wheel against taglib-1.11.1
- cython version used to create the shipped cpp-file updated to 0.25.1

## pytaglib 1.3.0 (2016/07/22)

- Remove workaround for pre-1.9 taglib versions in order to reduce codebase
- code cleanup
- move tests out of source folder

## pytaglib 1.2.1 (2016/07/17)

This is a non-feature release (no change to the code base)

- update README
- build windows wheel against taglib 1.11

## pytaglib 1.2.0 (2016/03/20)

- add Windows support (see README)
- update copyright dates
- update cython version used to build shipped taglib.cpp to 0.23.4

## pytaglib 1.1.0 (2015/09/06)

- add a `File.close()` method that ends all I/O operations.

## pytaglib 1.0.3 (2015/03/16)

- include ReST version of the README for pypi (converted using pandoc)

## pytaglib 1.0.2 (2015/03/15)

- ensure that pyprinttags removes unsupported properties only when user enters 'y' or 'yes'
  (thanks to lahwaacz)
- fix a typo in the readme (thanks to panzl)

## pytaglib 1.0.1 (2015/03/09)

- cleaned up source code and made it more readable
- update README to contain more information
- no functional API changes

## pytaglib 1.0 (2015/01/03)

- as the library has been used for several years now without any known
  bugs, I declare it as stable.
- cleaned up source. Especially simplified several statements due to improvements
  in recent Cython versions.
- The workaround for MPEG files with taglib <= 1.8 is now forced disabled if taglib version >= 1.9
  is detected.
- update copyright dates

## pytaglib 0.4 (2014/03/29)

- remove Cython dependency by shipping taglib.cpp

## pytaglib 0.3.7 (2014/01/21)

- remove a test file that looked a little non-free
- update copyright dates

## pytaglib 0.3.6 (2013/08/13)

- fix Python 2.6 support in pyprinttags
- update copyright dates

## pytaglib 0.3.5 (2013/04/03)

- add support for Python 2.6 by replacing some methods added in 2.7

## pytaglib 0.3.4 (2013/01/16)

- move cython from install_requires to setup_requires

## pytaglib 0.3.3 (2013/01/16)

- ensure sources are included in sdist packages
- fix call to pyprinttags
- fix setup.py handling for non-utf8-locales
- rename pyprinttags to pyprinttags3 for python3 installs

## pytaglib 0.3.2 (2013/01/12)

- add "batch mode" to pyprinttags and allow several files at once
- add a man page for pyprinttags
- remove .travis.yml since travis' build system is too old for building pytaglib

## pytaglib 0.3.1 (2013/01/07)

- updated packaging information in setup.py

## pytaglib 0.3.0 (2012/12/14)

- implement a hack that works around a bug in taglib, leading
  to several problems in connection with MP3 files with ID3v1
  tags. Open files with `f=taglib.File(path, applyID3v2Hack=True)`
  to ensure that MPEG files will always get updated to ID3v2 if
  necessary. Use at your own risk!
- update documentation
- declare development stadium as "beta" since no critical bugs
  seem to exist.

## pytaglib 0.2.5 (2012/12/05)

- fix integration into PyPI, clean up code & documentation

## pytaglib 0.2.4 (2012/09/09)

- add test script for python2.x/3.x

## pytaglib 0.2.3 (2012/07/30)

- save() now returns unsuccessful tags due to metadata format
- add taglib.version attribute to get module version
- all tests pass with my taglib fork
- fix Python2 compatibility
- README now in ReSt format
- code cleanup and documentation improvement

## pytaglib 0.2.2 (2012/07/25)

- Switch to setuptools/distribute, prepare publishing on PyPI
- Add some basic unit tests (test files stolen from taglib)
- Ensure package works with Python2.x/3.x
