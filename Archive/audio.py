#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import subprocess

max_volume = 100
diff = 5

def getDevices():
    devices = subprocess.run("pacmd list-sinks", capture_output=True, text=True, shell=True)
    iterable = re.finditer(r"name: <([a-zA-Z0-9._-]+)>", devices.stdout)
    return [sink[1] for sink in iterable]
def getVolume(device):
    command = subprocess.run(f"pactl get-sink-volume {device}",
                         capture_output=True, text=True, shell=True)
    iterable = re.finditer(r" ([0-9]+)%", command.stdout)
    right_left_vol = [item[1] for item in iterable]
    return int(right_left_vol[0])
def getMute(device):
    mute_status = subprocess.run(f"pactl get-sink-mute {device}",
                             capture_output=True, text=True, shell=True)
    if mute_status.stdout == "Mute: no\n":
        return False
    else:
        return True
def notifyVolume(volume, muteflag=False):
    # Play volume change sound
    subprocess.run(
        'canberra-gtk-play -i audio-volume-change -d "changeVolume"',
        shell=True
    )
    # Send actual notification
    ID =9993
    if volume == 0 or muteflag:
        icon = "audio-volume-muted"
        message = "Volume muted"
    else:
        icon = "audio-volume-high"
        message = f"Volume: {volume}%"
    subprocess.run(
        f'dunstify -a volumectl -u low -r "{ID}" -h int:value:{volume} -i {icon} "{message}" -t 2000',
        shell=True
    )
