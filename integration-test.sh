#!/bin/bash

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

FILE_NAME=`./getBinaryName.sh`
chmod +x ./dist/$FILE_NAME

declare -a lines_to_find=("detected java code. we recommend using Corretto"
                "detected python code. min version 3.7.5 is required"
                "detected python code. if you need pip, version 19.3 or above is recommended"
                "using dependency library openblas version 0.3.16. upgrade to at least version 0.3.17"
                "dependency library numpy is present. min version 1.19.0 is required"
                "detected java code. min version 8 is required. version 11 or above is recommended"
                "using dependency library snappy-java version 1.1.3. upgrade to at least version 1.1.4"
                "using dependency library hadoop-lzo. this library requires a manual build"
                "dependency library: leveldbjni-all is not supported on Graviton"
                "detected go code. min version 1.16 is required. version 1.18 or above is recommended"
                "using dependency library github.com/golang/snappy version 0.0.1. upgrade to at least version 0.0.2"
                )

echo "Running samples to console"
./dist/$FILE_NAME ./sample-projects/ > console_test.txt
test_report 'console' 'console_test.txt' "${lines_to_find[@]}"
rm console_test.txt


echo "Running samples to HTML report"
./dist/$FILE_NAME ./sample-projects/ --output test.html
test_report 'html' 'test.html' "${lines_to_find[@]}"
rm test.html


echo "Running samples to Dependency Report"
declare -a dependencies=("<si><t>component</t></si><si><t>version</t></si><si><t>origin</t></si><si><t>filename</t></si>"
                        "<si><t>junit</t></si><si><t>4.8.2</t></si>"
                        "<si><t>zstd-jni</t></si><si><t>1.1.0</t></si>"
                        "<si><t>snappy-java</t></si><si><t>1.1.3</t></si>"
                        "<si><t>lz4-java</t></si><si><t>1.4.0</t></si>"
                        "<si><t>hadoop-lzo</t></si><si><t>0.4.17</t></si>"
                        "<si><t>leveldbjni-all</t></si><si><t>1.8</t></si>"
                        "<si><t>CommandLineParser</t></si><si><t>2.8.0</t></si>"
                        "<si><t>Microsoft.Build.Utilities.Core</t></si><si><t>17.1.0</t></si>"
                        "<si><t>Microsoft.Extensions.Logging.Console</t></si><si><t>6.0.0</t></si>"
                        "<si><t>Microsoft.NET.Test.Sdk</t></si><si><t>16.5.0</t></si>"
                        "<si><t>Microsoft.VisualStudio.Setup.Configuration.Interop</t></si><si><t>3.1.2196</t></si>"
                        "<si><t>System.Linq.Async</t></si><si><t>6.0.1</t></si>"
                        "<si><t>xunit</t></si><si><t>2.4.1</t></si>"
                        "<si><t>coverlet.collector</t></si><si><t>1.2.0</t></si>"
                        "<si><t>OpenBLAS</t></si>"
                        "<si><t>SciPy</t></si>"
                        "<si><t>NumPy</t></si>"
                        "<si><t>FakeDependency</t></si><si><t>1.2.3</t></si>"
                        "<si><t>0.3.17</t></si>"
                        "<si><t>cors</t></si><si><t>2.8.5</t></si>"
                        "<si><t>express</t></si><si><t>4.18.1</t></si>"
                        "<si><t>rxjs</t></si><si><t>7.5.6</t></si>"
                        "<si><t>socket.io</t></si><si><t>4.5.1</t></si>"
                        "<si><t>@codechecks/client</t></si><si><t>0.1.12</t></si>"
                        "<si><t>@commitlint/cli</t></si><si><t>17.0.3</t></si>"
                        "<si><t>eslint</t></si><si><t>7.32.0</t></si>"
                        "<si><t>typescript</t></si><si><t>4.7.4</t></si>"
                        "<si><t>github.com/aws/aws-sdk-go</t></si>"
                        "<si><t>github.com/golang/snappy</t></si>"
                        "<si><t>rails</t></si><si><t>6.1.6.1</t></si>"
                        "<si><t>rake</t></si><si><t>11.1</t></si>"
                        "<si><t>actionpack</t></si>"
                        "<si><t>bcrypt</t></si><si><t>3.1</t></si>"
                        "<si><t>cucumber</t></si><si><t>4.1</t></si>"
                        "<si><t>gc_tracer</t></si>"
                        "<si><t>gssapi</t></si>"
                        "<si><t>mail</t></si>"
                        "<si><t>turbo-rails</t></si>"
                        "<si><t>httpclient</t></si>"
                        "<si><t>jruby-openssl</t></si>"
                    )
./dist/$FILE_NAME ./sample-projects/ --output test.xlsx --output-format dependencies
# xlsx files are compressed files, so we need to unzip them and then compare them
mkdir ./temp
unzip -q ./test.xlsx -d ./temp
test_report 'dependencies' './temp/xl/sharedStrings.xml' "${dependencies[@]}"
rm test.xlsx
rm -rf ./temp


echo "--- Running negative tests ---"

echo "Running missing arguments test"
./dist/$FILE_NAME 2>&1 | tee missing_arguments_test.txt
if diff "./tests-baseline/missing_arguments_test.txt" "missing_arguments_test.txt"; then
    echo "**PASSED** missing arguments test"
else
    echo "**FAILED**: missing arguments test" && exit 1 
fi
rm missing_arguments_test.txt


echo "Running directory not found test"
./dist/$FILE_NAME unexisting_directory 2>&1 | tee directory_not_found_test.txt
if diff "./tests-baseline/directory_not_found_test.txt" "directory_not_found_test.txt"; then
    echo "**PASSED** directory not found test"
else
    echo "**FAILED**: directory not found test" && exit 1 
fi
rm directory_not_found_test.txt