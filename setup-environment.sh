#!/bin/bash

# This script looks up Python 3.10 or higher in PATH and sets up the Python Virtual Environment to install dependencies

for AVAILABLE_PYTHON in $(compgen -c python | sort -u); do
    PYTHON_VERSION_MAJOR=$($AVAILABLE_PYTHON --version 2>/dev/null | awk -F '[ .]' 'BEGIN {OFS="."} {print $(NF-2)}')
    PYTHON_VERSION_MINOR=$($AVAILABLE_PYTHON --version 2>/dev/null | awk -F '[ .]' 'BEGIN {OFS="."} {print $(NF-1)}')
    if [[ $PYTHON_VERSION_MAJOR -ge 3 ]] && [[ $PYTHON_VERSION_MINOR -ge 10 ]]; then
	    PYTHON3=$AVAILABLE_PYTHON
	    echo "🐍 python3.10+ is installed"
   	  break
    fi
done

if [[ ! -z $PYTHON3 ]]
then
    if hash pip3
    then
        echo "📦 pip is installed"
    else
        echo "**ERROR**: python pip3 not found, please install pip3" && exit 1
    fi

    if [ ! -f ".venv/bin/activate" ]; then
        echo "💻 Creating Python virtual environment"
        $PYTHON3 -m venv .venv
        if [ $? -ne 0 ]; then
            echo "**ERROR**: could not create Python Virtual Environment." && exit 1
        fi
    fi
    
    echo "💡 Making sure Python Virtual Environment is active"
    . .venv/bin/activate
    if [ $? -ne 0 ]; then
        echo "**ERROR**: could not activate Python Virtual Environment." && exit 1
    fi
    
    echo "☁️ Installing requirements"
    $PYTHON3 -m pip install -r requirements-build.txt
    if [ $? -ne 0 ]; then
        echo "**ERROR**: error installing required packages" && exit 1
    fi
    exit 0
else
    echo "**ERROR**: python3.10+ is missing, please install it before running this build script"
    exit 1
fi

