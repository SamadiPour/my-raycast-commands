#!/usr/bin/python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title B612 Status
# @raycast.mode inline
# @raycast.refreshTime 5m

# Optional parameters:
# @raycast.icon https://upload.wikimedia.org/wikipedia/en/thumb/0/04/Huawei_Standard_logo.svg/2016px-Huawei_Standard_logo.svg.png

# Documentation:
# @raycast.description Getting internet status from B612 Modem
# @raycast.author Amir Hossein SamadiPour
# @raycast.authorURL https://github.com/SamadiPour

import datetime
import os
import shelve
import sys
import time
from functools import partial
import subprocess

from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
from mac_notifications import client as notif

rat_mapping = {
    '0': '2G',
    '2': '3G',
    '7': '4G',
    '': 'auto',
}
USERNAME = 'admin'
PASSWORD = 'password'
IP = '192.168.10.1'
SHOW_NOTIFICATION = True
NOTIFICATION_ACTION = False


def app_folder(prog: str) -> str:
    if sys.platform == "win32":
        directory = os.path.join(os.path.expanduser("~"), "AppData", "Local", prog)
    else:
        directory = os.path.join(os.path.expanduser("~"), "." + prog)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def save_key(key, value):
    path = os.path.join(app_folder('scripts_data'), '.b612db')
    with shelve.open(path) as db:
        db[key] = value
    pass


def load_key(key, default=None):
    path = os.path.join(app_folder('scripts_data'), '.b612db')
    with shelve.open(path) as db:
        try:
            value = db[key]
        except:
            value = None
        finally:
            return default if value is None else value
    pass


def reboot(conf_number: int | str) -> None:
    with Connection(f'http://{USERNAME}:{PASSWORD}@{IP}/') as reboot_conn:
        reboot_client = Client(reboot_conn)
        reboot_client.device.reboot()
    os._exit(1)


if __name__ == "__main__":
    try:
        with Connection(f'http://{USERNAME}:{PASSWORD}@{IP}/') as connection:
            client = Client(connection)
            statistics = client.monitoring.month_statistics()
            plmn = client.net.current_plmn()
            upDown = (int(statistics['CurrentMonthDownload']) + int(statistics['CurrentMonthUpload'])) / 1000 / 1000 / 1000
            ip = client.device.information()['WanIPAddress']

            operator = plmn.get('FullName', 'No Operator')
            mode = rat_mapping.get(plmn.get('Rat', '-1'), None)

            command = "traceroute -d -m 2 1.1.1.1 2>&1 | tail -n 1 | awk '{print $2}'"
            trace_result = subprocess.check_output(command, shell=True, timeout=10).decode('utf-8').strip()

            output = (operator
                    + (f' {mode}' if mode is not None else '')
                    + (' - No IP' if ip is None else '')
                    + (' - No Route' if trace_result != '192.168.10.1' else '')
                    + ' - ' + str(round(upDown, 2)) + ' GB')
            print(output)

            # showing notification
            if SHOW_NOTIFICATION and (ip is None or mode != '4G' or operator.lower() != 'samantel' or trace_result != '192.168.10.1'):
                now = datetime.datetime.now()
                last_time = load_key('last_notification')
                if last_time is not None and now - last_time <= datetime.timedelta(minutes=10):
                    exit()

                save_key('last_notification', now)
                notif.create_notification(
                    title=output,
                    action_button_str="Reboot" if NOTIFICATION_ACTION else None,
                    action_callback=partial(reboot, conf_number='123123') if NOTIFICATION_ACTION else None,
                )
                if NOTIFICATION_ACTION:
                    time.sleep(30)
                    notif.stop_listening_for_callbacks()
    except Exception as e:
        print(e)
