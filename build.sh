#!/bin/bash

# This script converts the porting-advisor python code into
# a x86 or arm64 Linux or Mac binary like a.out.
# As a prerequisite, pip3 must already be installed
# The resulting native binary does not need sudo to execute.

if [ ! -f ".venv/bin/activate" ]; then
    ./setup-environment.sh
fi

. .venv/bin/activate

if [[ -z "${FILE_NAME}" ]]; then
  FILE_NAME=`./getBinaryName.sh`
else
  FILE_NAME="${FILE_NAME}"
fi

echo "*** Will use $FILE_NAME as name ***"

if hash mvn
then
    mvn package --file ./src/advisor/tools/graviton-ready-java/pom.xml
    if [ $? -ne 0 ]; then
        echo "**ERROR**: error generating jar for Graviton Ready Java tool" && exit 1
    fi
fi

echo "🏗️ Generating executable"
CERT_PATH=$(python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')
pyinstaller --onefile --clean --noconfirm --distpath dist --add-data 'src/advisor/rules/*.json:advisor/rules' --add-data 'src/advisor/tools/graviton-ready-java/target/*:advisor/tools/graviton-ready-java/target' --add-data 'src/advisor/templates/template.html:advisor/templates' --add-data "$CERT_PATH/certifi/cacert.pem:certifi" --name "$FILE_NAME" "src/porting-advisor.py" --exclude-module readline
if [ $? -ne 0 ]; then
    echo "**ERROR**: pyinstaller failed, binary was not created" && exit 1
fi
echo 🎉 "*** Success: Executable saved at dist/$FILE_NAME ***"
exit 0