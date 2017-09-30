#!/bin/bash
# inspired by GOG

ABS=`realpath $1`
SCRIPTCWD=`realpath "$( dirname $0 )"`

# clean-up
find $ABS/venv $ABS/data -iname "*.py[oc]" -delete

# pack the stuff :-p
cd $ABS || { echo "Oh no, cant cd to $ABS"; exit 1; }
tar czf asdf.tgz venv data

# SFX magic
DATE=`date +%s`
NAME="runme-v$DATE.sh"
sed s:##target_path##:$ABS:g $SCRIPTCWD/installer_prefix | cat - asdf.tgz > $NAME
chmod u+x $NAME
rm asdf.tgz
