#!/usr/bin/python
# -*- coding: utf-8 -*-
import backlight
import subprocess

brightness = backlight.getBrightness()
if brightness <= backlight.diff:
    subprocess.run(f"xbacklight -set {backlight.diff}", shell=True)
else:
    subprocess.run(f"xbacklight -dec {backlight.diff}", shell=True)

brightness = backlight.getBrightness()
if brightness < backlight.diff:
    brightness = 0
backlight.notifyBrightness(brightness)
