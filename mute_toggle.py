#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import audio

subprocess.run(
    "wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle",
    shell=True
)
volume, mute = audio.getStatus()
audio.notifyVolume(volume, muteflag=mute)
