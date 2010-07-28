#!/bin/bash

pyfiles=`find -name "*.py"`
for file in $pyfiles;
do
    first_line=`head -n 1 $file`
    if grep -q '^#!' <<< $first_line;
    then
        echo chmod +x $file;
        chmod +x $file;
    fi;
done;
