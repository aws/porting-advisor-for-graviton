#!/bin/sh

# Runs unit tests, generates the binary and then runs it against sample projects

# run unit tests
echo "🐍 Setup virtual environment"
./setup-environment.sh
if [ $? -ne 0 ]; then
    echo "**ERROR**: failed to initialize Python Virtual Environment" && exit 1
fi

# run unit tests
echo "🔬 Running unit tests"
./unit-test.sh
if [ $? -ne 0 ]; then
    echo "**ERROR**: unit tests failed" && exit 1
fi

# build project
echo "⚒️ Building project"
./build.sh
if [ $? -ne 0 ]; then
    echo "**ERROR**: failed to build project" && exit 1
fi

echo "🧪 Running integration tests"
./integration-test.sh
if [ $? -ne 0 ]; then
    echo "**ERROR**: integration tests failed" && exit 1
fi