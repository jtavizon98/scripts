#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import audio

current_volume, mute = audio.getStatus()
if current_volume < audio.diff:
    subprocess.run(
        "wpctl set-volume @DEFAULT_AUDIO_SINK@ 0%",
        shell=True
    )
    current_volume = 0
else:
    subprocess.run(
        f"wpctl set-volume @DEFAULT_AUDIO_SINK@ {audio.diff}%-",
        shell=True
    )
    current_volume -= audio.diff
audio.notifyVolume(current_volume, muteflag=mute)
