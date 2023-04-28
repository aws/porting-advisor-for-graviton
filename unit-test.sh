#!/bin/sh

echo "🐍 Making sure Python Virtual Environment is active"
. .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "**ERROR**: could not activate Python Virtual Environment." && exit 1
fi

# run unit tests
echo "🔬 *** running unit tests ***"
python -m coverage run --source=./src -m unittest discover -s unittest -p "test_*.py" -v
if [ $? -ne 0 ]; then
    echo "**ERROR**: unit tests failed" && exit 1
fi