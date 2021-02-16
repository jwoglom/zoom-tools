#!/bin/bash

osascript -e 'property muteAudio : "Stop Video"
property unmuteAudio : "Start Video"

if application "zoom.us" is running then
	tell application "System Events"
		tell application process "zoom.us"
			if exists (menu item muteAudio of menu 1 of menu bar item "Meeting" of menu bar 1) then
				click menu item muteAudio of menu 1 of menu bar item "Meeting" of menu bar 1
				set returnValue to "Video off"
			else
				set returnValue to "Video already off"
			end if
		end tell
	end tell
else
	set returnValue to ""
end if

return returnValue'