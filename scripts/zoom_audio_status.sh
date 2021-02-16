#!/bin/bash
osascript -e 'property btnTitle : "Mute audio"

if application "zoom.us" is running then
  tell application "System Events"
      tell application process "zoom.us"
          if exists (menu item btnTitle of menu 1 of menu bar item "Meeting" of menu bar 1) then
              set returnValue to "Audio on"
          else
              set returnValue to "Audio off"
          end if
      end tell
  end tell
else
  set returnValue to ""
end if

return returnValue'