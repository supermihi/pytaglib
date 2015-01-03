#!/bin/sh
rm src/taglib.cpp
rm src/taglib*.so
echo "Running python2 test ..."
python2 setup.py test --cython
echo "Python2 test done. Press [Enter]"

read
rm src/taglib.cpp
rm src/taglib*.so
echo "Running python3 test ..."
python3 setup.py test --cython
