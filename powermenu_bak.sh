#!/usr/bin/env bash

set -e
set -u

#chosen=$(printf " Shut Down\n Restart\n Suspend\n Hibernate\n Lockscreen" | rofi -dmenu -i -theme-str '@import "power.rasi"')
chosen=$(printf " Shut Down\n Restart\n Suspend\n Hibernate\n Lockscreen" | rofi -dmenu -i)

case "$chosen" in
        " Shut Down") systemctl poweroff;;
        " Restart") systemctl reboot;;
        " Suspend") systemctl suspend;;
        " Hibernate") systemctl hibernate;;
        #" Logout") python ~/.scripts/logout-qtile.py;;
        " Lockscreen") dm-tool lock;;
        *) exit 1;;
esac
