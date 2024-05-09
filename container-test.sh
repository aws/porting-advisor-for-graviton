#!/bin/bash

source ./test-helpers.sh

# This script tests container image build and runs a couple of
# tests against the generated image.

echo "Setting up sample-projects"
sample_project_directory=$(get_sample_projects_relative_path)

docker build -t porting-advisor .
if [ $? -ne 0 ]; then
    echo "**ERROR**: building container image" && exit 1
fi

echo "Running container on samples to console"
docker run --rm -v $(pwd)/$sample_project_directory:/source porting-advisor /source > console_test.txt
test_report 'console' 'console_test.txt' "${lines_to_find[@]}"
if [ $? -ne 0 ]; then
    echo "**ERROR**: running container to console" && exit 1
fi
rm console_test.txt

echo "Running container on samples to HTML report"
docker run --rm -v $(pwd):/source porting-advisor /source/$sample_project_directory --output /source/test.html 
test_report 'html' 'test.html' "${lines_to_find[@]}"
if [ $? -ne 0 ]; then
    echo "**ERROR**: running container to html report" && exit 1
fi
rm -f test.html

exit 0
