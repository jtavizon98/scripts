#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import audio

current_volume, mute = audio.getStatus()
if audio.max_volume <= (current_volume + audio.diff):
    subprocess.run(
        f"wpctl set-volume @DEFAULT_AUDIO_SINK@ 100%",
        shell=True
    )
    current_volume = audio.max_volume
else:
    subprocess.run(
        f"wpctl set-volume @DEFAULT_AUDIO_SINK@ {audio.diff}%+",
        shell=True
    )
    current_volume += audio.diff
audio.notifyVolume(current_volume, mute)


