#!/usr/bin/osascript

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Toggle Desktop Icons
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🖥️
# @raycast.packageName System

# Documentation:
# @raycast.description Toggle showing icons on the desktop.
# @raycast.author Amir Hossein SamadiPour
# @raycast.authorURL https://github.com/SamadiPour

if (do shell script "defaults read com.apple.finder CreateDesktop") is equal to "1" then
    do shell script "defaults write com.apple.finder CreateDesktop -bool false"
else
    do shell script "defaults write com.apple.finder CreateDesktop -bool true"
end if

do shell script "killall Finder"
