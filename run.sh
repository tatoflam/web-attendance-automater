#!/bin/bash
export PATH=/Users/tato/repo/github/tatoflam/web-attendance-automater:$PATH
SCRIPT_DIR=$(cd $(dirname $0); pwd) 
cd $SCRIPT_DIR
source $SCRIPT_DIR/env1/bin/activate
$SCRIPT_DIR/env1/bin/python web-attendance-automater.py
deactivate
