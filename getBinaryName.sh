#!/bin/bash

# get binary name
OS_SUFFIX="Other"
case "$(uname -s)" in
    Darwin)
        OS_SUFFIX="macosx"
        ;;

    Linux)
        OS_SUFFIX="linux"
        ;;
esac

if [ $OS_SUFFIX = "Other" ]
then
    echo "**ERROR**: Unsupported platform" && exit 1
fi

PROCESSOR_SUFFIX=`uname -m`
FILE_NAME="porting-advisor-$OS_SUFFIX-$PROCESSOR_SUFFIX"
echo $FILE_NAME