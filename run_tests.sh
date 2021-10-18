#!/bin/bash

for test_case in $(ls configs|cut -f1 -d'.'|grep -v "__")
do
    echo running $test_case
    python3.7 -m da --message-buffer-size 50000 --no-log src/run.da $test_case
done
    
