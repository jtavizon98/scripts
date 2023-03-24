#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import subprocess

touchpad = "VEN_04F3:00 04F3:3242 Touchpad"

def getStatus(device):
    command = subprocess.run(
        f'xinput list-props "{device}" | grep "Device Enabled"',
        shell=True, capture_output=True, text=True
    )
    status_str = re.search(r":\t(0|1)", command.stdout)
    status = int(status_str.group(0).replace(":\t", ''))
    return bool(status)

if getStatus(touchpad):
    subprocess.run(f'xinput disable "{touchpad}"', shell=True)
    subprocess.run('dunstify -a toggleTouchpad -u low -r 9995  -i input-touchpad-off "Touchpad off"',
                   shell=True)
else:
    subprocess.run(f'xinput enable "{touchpad}"', shell=True)
    subprocess.run('dunstify -a toggleTouchpad -u low -r 9995  -i input-touchpad-on "Touchpad on"',
                   shell=True)
