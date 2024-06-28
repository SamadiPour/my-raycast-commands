#!/usr/bin/python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title B612 Reboot
# @raycast.mode silent

# Optional parameters:
# @raycast.icon https://upload.wikimedia.org/wikipedia/en/thumb/0/04/Huawei_Standard_logo.svg/2016px-Huawei_Standard_logo.svg.png

# Documentation:
# @raycast.description Rebooting B612 Modem
# @raycast.author Amir Hossein SamadiPour
# @raycast.authorURL https://github.com/SamadiPour

from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection

USERNAME = 'admin'
PASSWORD = 'password'
IP = '192.168.10.1'
with Connection(f'http://{USERNAME}:{PASSWORD}@{IP}/') as connection:
    client = Client(connection)
    client.device.reboot()
