#!/bin/bash

# This script sets up the Python Virtual Environment to install dependencies

if hash python3
then
    echo "🐍 python3 is installed"

    if hash pip3
    then
        echo "📦 pip is installed"
    else
        echo "**ERROR**: python pip3 not found, please install pip3" && exit 1
    fi

    if [ ! -f ".venv/bin/activate" ]; then
        echo "💻 Creating Python virtual environment"
        python3 -m venv .venv
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
    python3 -m pip install -r requirements-build.txt
    if [ $? -ne 0 ]; then
        echo "**ERROR**: error installing required packages" && exit 1
    fi
    exit 0
else
    echo "**ERROR**: python3 is missing, please install it before running this build script"
    exit 1
fi