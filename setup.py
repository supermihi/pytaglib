from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("taglib", ["src/taglib.pyx", "src/ctypes.pxd"],
                         libraries=['tag', "stdc++"],
                         language="c++",
                         extra_compile_args=["-fpermissive"])]

setup(
  name = 'TagLib bindings for python, using cython',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules,
)
