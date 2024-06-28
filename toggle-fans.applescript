#!/usr/bin/osascript

# @raycast.title Toggle Fans
# @raycast.author Amir Hossein SamadiPour
# @raycast.authorURL https://github.com/SamadiPour
# @raycast.description Toggle Fans using Macs Fan Control app

# @raycast.icon images/fan.png
# @raycast.mode silent
# @raycast.packageName Macs Fan Control
# @raycast.schemaVersion 1

on is_running(appName)
	tell application "System Events" to (name of processes) contains appName
end is_running

set isRunning to is_running("Macs Fan Control")
if isRunning then
	try
		tell application "Macs Fan Control"
			quit
		end tell
	end try
else
	try
		tell application "Macs Fan Control"
			launch
		end tell
	end try
end if
