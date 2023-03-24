#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import audio

current_volume = 0
for device in audio.getDevices():
    current_volume = audio.getVolume(device)
    if (audio.max_volume-audio.diff)< current_volume:
        subprocess.run(["pactl", "set-sink-volume", device, f"{audio.max_volume}%"])
        current_volume = audio.max_volume
    else:
        subprocess.run(["pactl", "set-sink-volume", device, f"+{audio.diff}%"])
        current_volume += audio.diff
audio.notifyVolume(current_volume)


