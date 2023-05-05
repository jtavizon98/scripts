#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import subprocess

max_volume = 100
diff = 5

def getStatus():
    command = subprocess.run(f"wpctl get-volume @DEFAULT_AUDIO_SINK@",
                         capture_output=True, text=True, shell=True)
    capture = re.search(r"(\[[A-Z]+\])", command.stdout)
    try:
        if capture.group(1) == "[MUTED]":
            muteflag = True
    except AttributeError:
        muteflag = False
    volume  = float(re.search(r" ([012]\.[0-9]+)", command.stdout).group(1))
    volume = int(volume*1e2)
    return volume, muteflag
def notifyVolume(volume, muteflag=False):
    # Play volume change sound
    subprocess.run(
        'canberra-gtk-play -i audio-volume-change -d "changeVolume"',
        shell=True
    )
    # Send actual notification
    ID =9993
    if volume == 0 or muteflag:
        message = "󰸈 Volume muted"
    else:
        message = f"󰕾 Volume: {volume}%"
    subprocess.run(
        f'dunstify -a volumectl -u low -r "{ID}" -h int:value:{volume} "{message}" -t 2000',
        shell=True
    )

if __name__ == '__main__':
    getStatus()
