#!/bin/bash

mkdir build
cd build
wget https://results.enr.clarityelections.com//PA/Allegheny/111176/281494/reports/detailxml.zip
# wget https://results.enr.clarityelections.com//PA/Allegheny/109361/277443/reports/detailxml.zip
unzip detailxml.zip
python3 ../scripts/process_scytl.py
cd ..
