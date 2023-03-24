#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import audio

current_volume = 0
for device in audio.getDevices():
    current_volume = audio.getVolume(device)
    if current_volume < audio.diff:
        subprocess.run(["pactl", "set-sink-volume", device, "0%"])
        current_volume = 0
    else:
        subprocess.run(["pactl", "set-sink-volume", device, f"-{audio.diff}%"])
        current_volume -= audio.diff
audio.notifyVolume(current_volume)
