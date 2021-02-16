#!/bin/bash

osascript -e 'property muteAudio : "Mute audio"
property unmuteAudio : "Unmute audio"

if application "zoom.us" is running then
	tell application "System Events"
		tell application process "zoom.us"
			if exists (menu item muteAudio of menu 1 of menu bar item "Meeting" of menu bar 1) then
				set returnValue to "Audio on"
			else
				click menu item unmuteAudio of menu 1 of menu bar item "Meeting" of menu bar 1
				set returnValue to "Audio on"
			end if
		end tell
	end tell
else
	set returnValue to ""
end if

return returnValue'