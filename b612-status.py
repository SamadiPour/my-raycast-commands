#!/usr/bin/python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title B612 Status
# @raycast.mode inline
# @raycast.refreshTime 15m

# Optional parameters:
# @raycast.icon https://upload.wikimedia.org/wikipedia/en/thumb/0/04/Huawei_Standard_logo.svg/2016px-Huawei_Standard_logo.svg.png

# Documentation:
# @raycast.description Getting internet status from B612 Modem
# @raycast.author Amir Hossein SamadiPour
# @raycast.authorURL https://github.com/SamadiPour

from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection

rat_mapping = {
    '0': '2G',
    '2': '3G',
    '7': '4G',
    '': 'auto',
}

USERNAME = 'admin'
PASSWORD = 'password'
IP = '192.168.10.1'
with Connection(f'http://{USERNAME}:{PASSWORD}@{IP}/') as connection:
    client = Client(connection)
    statistics = client.monitoring.month_statistics()
    plmn = client.net.current_plmn()
    upDown = (int(statistics['CurrentMonthDownload']) + int(statistics['CurrentMonthUpload'])) / 1000 / 1000 / 1000
    ip = client.device.information()['WanIPAddress']

    operator = plmn.get('FullName', 'No Operator')
    mode = rat_mapping.get(plmn.get('Rat', '-1'), None)
    print(
        operator
        + (f' {mode}' if mode is not None else '')
        + (' - No IP' if ip is None else '')
        + ' - ' + str(round(upDown, 2)) + ' GB'
        )
