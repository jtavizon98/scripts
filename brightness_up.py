#!/usr/bin/python
# -*- coding: utf-8 -*-
import backlight
import subprocess

subprocess.run(f"xbacklight -inc {backlight.diff}", shell=True)

brightness = backlight.getBrightness()
if brightness < backlight.diff:
    brightness = 100
backlight.notifyBrightness(brightness)
