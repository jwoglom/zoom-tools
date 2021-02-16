#!/bin/bash

launchctl unload ~/Library/LaunchAgents/jwoglom.zoomtoolsclient.plist || true
rm -rf ~/Library/LaunchAgents/jwoglom.zoomtoolsclient.plist || true

ln -s `pwd`/jwoglom.zoomtoolsclient.plist ~/Library/LaunchAgents/
launchctl load -w ~/Library/LaunchAgents/jwoglom.zoomtoolsclient.plist
launchctl start -w ~/Library/LaunchAgents/jwoglom.zoomtoolsclient.plist

