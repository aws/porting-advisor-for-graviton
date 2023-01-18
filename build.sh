#!/bin/sh

# This script converts the porting-advisor python code into
# a x86 or arm64 Linux or Mac binary like a.out.
# As a prerequisite, pip3 must already be installed
# The resulting native binary does not need sudo to execute.

if hash python3
then
    echo "python3 is installed"

    if hash pip3
    then
        echo "pip is installed"
    else
        echo "**ERROR**: python pip3 not found, please install pip3" && exit 1
    fi

    FILE_NAME=`./getBinaryName.sh`
    echo "*** Will use $FILE_NAME as name ***"

    if [ ! -f ".venv/bin/activate" ]; then
        echo "Creating Python virtual environment"
        python3 -m venv .venv
        if [ $? -ne 0 ]; then
            echo "**ERROR**: could not create Python Virtual Environment." && exit 1
        fi
    fi
    
    echo "Making sure Python Virtual Environment is active"
    . .venv/bin/activate
    if [ $? -ne 0 ]; then
        echo "**ERROR**: could not activate Python Virtual Environment." && exit 1
    fi
    
    echo "Installing requirements"
    python3 -m pip install -r requirements-build.txt
    if [ $? -ne 0 ]; then
        echo "**ERROR**: error installing required packages" && exit 1
    fi

    if hash mvn
    then
        mvn package --file ./src/advisor/tools/graviton-ready-java/pom.xml
        if [ $? -ne 0 ]; then
            echo "**ERROR**: error generating jar for Graviton Ready Java tool" && exit 1
        fi
    fi

    echo "Generating executable"
    CERT_PATH=$(python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')
    pyinstaller --onefile --clean --noconfirm --distpath dist --add-data 'src/advisor/rules/*.json:advisor/rules' --add-data 'src/advisor/tools/graviton-ready-java/target/*:advisor/tools/graviton-ready-java/target' --add-data 'src/advisor/templates/template.html:advisor/templates' --add-data "$CERT_PATH/certifi/cacert.pem:certifi" --name "$FILE_NAME" "src/porting-advisor.py" --runtime-hook 'src/updater.py' --exclude-module readline
    if [ $? -ne 0 ]; then
       echo "**ERROR**: pyinstaller failed, binary was not created" && exit 1
    fi
    echo "*** Success: Executable saved at dist/$FILE_NAME ***"
    exit 0
else
    echo "**ERROR**: python3 is missing, please install it before running this build script"
    exit 1
fi
