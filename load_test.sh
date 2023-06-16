#!/bin/bash

FILE_NAME=`./getBinaryName.sh`
chmod +x ./dist/$FILE_NAME

git clone https://github.com/pytorch/pytorch.git
time ./dist/$FILE_NAME pytorch
rm -rf pytorch