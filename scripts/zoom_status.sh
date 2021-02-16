#!/bin/bash
osascript -e 'property muteBtnTitle : "Mute audio"
property videoBtnTitle : "Start Video"

if application "zoom.us" is running then
  tell application "System Events"
      tell application process "zoom.us"
          if exists (menu item muteBtnTitle of menu 1 of menu bar item "Meeting" of menu bar 1) then
              set muteReturnValue to "Audio on"
          else if exists (menu bar item "Meeting" of menu bar 1) then
              set muteReturnValue to "Audio off"
          else
              set muteReturnValue to "NotRunning"
          end if
          if exists (menu item videoBtnTitle of menu 1 of menu bar item "Meeting" of menu bar 1) then
              set videoReturnValue to "Video off"
          else if exists (menu bar item "Meeting" of menu bar 1) then
              set videoReturnValue to "Video on"
          else
              set videoReturnValue to "NotRunning"
          end if
      end tell
  end tell
else
  set muteReturnValue to "NotRunning"
  set videoReturnValue to "NotRunning"
end if

return {muteReturnValue, videoReturnValue}'