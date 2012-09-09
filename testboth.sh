#!/bin/sh
echo "Running python2 test ..."
python2 setup.py test
echo "Python2 test done. Press [Enter]"

read
echo "Running python3 test ..."
python3 setup.py test
