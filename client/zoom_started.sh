#!/bin/bash
FOLDER=$WMSCRIPTS/zoom-tools/client/
source $FOLDER/secrets.py

# Runs when a zoom meeting is started, and registers the local IP if present
LOCAL_IP=$(ifconfig|grep 192.168|sed 's/\(.*\)inet \(.*\) netmask \(.*\)/\2/g')
if [[ "$LOCAL_IP" != "" ]]; then
    (echo started; date; curl -X POST -d "ip=$LOCAL_IP&name=$(hostname)&token=$SELF_TOKEN" $ZOOMTOOLS_URL/register; echo) >> $FOLDER/log.log
fi