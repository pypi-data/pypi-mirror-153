#!/bin/sh

set -eux

cd src/contrast/assess_extensions/funchook

./autogen.sh
./configure
make

cp -f include/funchook.h ..
cp -f src/libfunchook.* ..

cd ../../../..
