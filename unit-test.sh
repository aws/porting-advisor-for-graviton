#!/bin/sh

# run unit tests
echo "*** running unit tests ***"
coverage run --source=./src -m unittest discover -s unittest -p "test_*.py" -v
if [ $? -ne 0 ]; then
    echo "**ERROR**: unit tests failed" && exit 1
fi