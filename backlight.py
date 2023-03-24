#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import subprocess

diff = 5

def getBrightness():
    command = subprocess.run(
        "xbacklight -get", 
        capture_output=True, text=True, shell=True
    )
    return int(command.stdout.replace("\n", ''))
def notifyBrightness(brightness):
    ID =9994
    message = f"󰃟  Brightness: {brightness}%"
    subprocess.run(
        f'dunstify -a xbacklight -u low -r "{ID}" -h int:value:{brightness} "{message}" -t 2000',
        shell=True
    )

