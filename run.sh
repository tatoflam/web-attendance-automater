#!/bin/bash
if [ "$#" != 1 ]
then 
  echo "No arguments were passed to the script."
else
  CURRENT_DIR=$(dirname "$0")
  export PATH=$CURRENT_DIR:$PATH
  SCRIPT_DIR=$(cd $(dirname $0); pwd) 
  cd $SCRIPT_DIR
  source $SCRIPT_DIR/env1/bin/activate
  $SCRIPT_DIR/env1/bin/python web-attendance-automater.py --parameter $1
  deactivate
fi
exit