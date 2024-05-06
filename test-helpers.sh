#!/bin/bash

function get_sample_projects_relative_path() {
    # Copy all sample projects to temp directory and rename project manifests to correct format.
    # This is done to avoid security scanning them for deprecated/vulnerable library dependancies
    # These sample projects are not intended to be used in production, but are used for testing
    sample_projects_dir=$RANDOM
    mkdir -p ./temp/$sample_projects_dir && cp -r ./sample-projects/* ./temp/$sample_projects_dir
    mv ./temp/$sample_projects_dir/dotnet-samples/sample_csproj_PLACEHOLDER ./temp/$sample_projects_dir/dotnet-samples/sample.csproj
    mv ./temp/$sample_projects_dir/go-samples/compatible/go_mod_PLACEHOLDER ./temp/$sample_projects_dir/go-samples/compatible/go.mod
    mv ./temp/$sample_projects_dir/go-samples/incompatible/go_mod_PLACEHOLDER ./temp/$sample_projects_dir/go-samples/incompatible/go.mod
    mv ./temp/$sample_projects_dir/java-samples/pom_xml_PLACEHOLDER ./temp/$sample_projects_dir/java-samples/pom.xml
    mv ./temp/$sample_projects_dir/node-samples/package_json_PLACEHOLDER ./temp/$sample_projects_dir/node-samples/package.json
    mv ./temp/$sample_projects_dir/python-samples/compatible/requirements_txt_PLACEHOLDER ./temp/$sample_projects_dir/python-samples/compatible/requirements.txt
    mv ./temp/$sample_projects_dir/python-samples/incompatible/requirements_txt_PLACEHOLDER ./temp/$sample_projects_dir/python-samples/incompatible/requirements.txt
    mv ./temp/$sample_projects_dir/ruby-samples/Gemfile_PLACEHOLDER ./temp/$sample_projects_dir/ruby-samples/Gemfile

    echo ./temp/$sample_projects_dir
}

function test_line() {
    reportType=$1
    result_filename=$2
    pattern=$3
    if grep --quiet "$3" "$result_filename"
    then
        echo "**PASS** $reportType report has: $pattern"
    else
        echo "**FAILED** $reportType report is missing: $pattern" && exit 1
    fi
}

function test_report() {
    report_type=$1
    shift
    result_filename=$1
    shift
    patterns=("$@")
    for line in "${patterns[@]}";
    do
        test_line $report_type $result_filename "${line[@]}"
    done
}

declare -a lines_to_find=("detected java code. we recommend using Corretto"
    "detected python code. min version 3.7.5 is required"
    "detected python code. if you need pip, version 19.3 or above is recommended"
    "dependency library numpy is present. min version 1.19.0 is required"
    "detected java code. min version 8 is required. version 11 or above is recommended"
    "using dependency library snappy-java version 1.1.3. upgrade to at least version 1.1.4"
    "using dependency library hadoop-lzo. this library requires a manual build"
    "dependency library: leveldbjni-all is not supported on Graviton"
    "detected go code. min version 1.16 is required. version 1.18 or above is recommended"
    "using dependency library github.com/golang/snappy version 0.0.1. upgrade to at least version 0.0.2"
)
