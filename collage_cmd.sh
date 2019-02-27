#!/bin/sh

#  collage_batch.sh
#  
#
#  Created by Suzanne Berger on 11/30/17.
#
MAYAPY=/Applications/Autodesk/maya2017/Maya.app/Contents/bin/mayapy
CMDPY=/Users/suzanneberger/bin/collage_cmd.py
#
$MAYAPY $CMDPY $*
