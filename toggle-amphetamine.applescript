#!/usr/bin/osascript

# Install Amphetamine via Mac App Store: https://apps.apple.com/us/app/amphetamine/id937984704

# @raycast.title Toggle Amphetamine
# @raycast.author Amir Hossein SamadiPour
# @raycast.authorURL https://github.com/SamadiPour
# @raycast.description Toggle Amphetamine Session

# @raycast.icon images/amphetamine.png
# @raycast.mode silent
# @raycast.packageName Amphetamine
# @raycast.schemaVersion 1

on is_running(appName)
	tell application "System Events" to (name of processes) contains appName
end is_running

set isRunning to is_running("Amphetamine")
if isRunning then
	tell application "Amphetamine" to end session
	do shell script "killall Amphetamine"
else
	tell application "Amphetamine" to start new session
end if
