#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Switch Router
# @raycast.mode inline

# Optional parameters:
# @raycast.icon 🛜

# Documentation:
# @raycast.description Switch policy for a device using mwan3 in OpenWRT routers
# @raycast.author Amir Hossein SamadiPour
# @raycast.authorURL https://github.com/SamadiPour


user="root"
ip="192.168.69.1"
first_policy="full"
second_policy="wanb_first"
device_name="mac_to"

ssh $user@$ip "uci get mwan3.${device_name}.use_policy | grep -q '${first_policy}' && uci set mwan3.${device_name}.use_policy='${second_policy}' || uci set mwan3.${device_name}.use_policy='${first_policy}' && /sbin/reload_config && uci commit"
result=$(ssh $user@$ip "uci get mwan3.${device_name}.use_policy")
echo "Current state: $result"