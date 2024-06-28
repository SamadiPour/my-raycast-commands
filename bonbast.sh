#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title bonbast
# @raycast.mode inline
# @raycast.refreshTime 3h

# Optional parameters:
# @raycast.icon 💰
# @raycast.packageName Bonbast

# Documentation:
# @raycast.description Getting prices from bonbast cli
# @raycast.author Amir Hossein SamadiPour
# @raycast.authorURL https://github.com/SamadiPour

function thousands {
    awk '{ printf("%'"'"'d\n",$1); }'
}

DATA="$(HTTPS_PROXY='127.0.0.1:2081' bonbast export | jq -r .)"
USD="$(echo "$DATA" | jq '.USD.buy' | thousands)"
EUR="$(echo "$DATA" | jq '.EUR.buy' | thousands)"
GBP="$(echo "$DATA" | jq '.GBP.buy' | thousands)"

echo "🇺🇸 USD: ${USD}  |  🇪🇺 EUR: ${EUR}  |  🇬🇧 GBP: ${GBP}"
