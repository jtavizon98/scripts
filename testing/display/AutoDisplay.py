#!/usr/bin/env python3

import subprocess
import time

def get_connected_displays():
    """Returns a list of connected displays using wlr-randr."""
    wlr_output = subprocess.check_output(['wlr-randr', '--list-monitors']).decode()
    connected_displays = []
    for line in wlr_output.splitlines():
        if 'connected' in line:
            display_name = line.split()[0]
            connected_displays.append(display_name)
    return connected_displays

def configure_display(display_name):
    """Configures the specified display using wlr-randr."""
    subprocess.run(['wlr-randr', '--output', display_name, '--auto'])

def restart_qtile():
    """Restarts the currently running Qtile session."""
    subprocess.run(['pkill', '-USR1', '-x', 'qtile'])

# Get the initial list of connected displays
connected_displays = get_connected_displays()

# Continuously check for changes in display connectivity
while True:
    time.sleep(5)
    new_connected_displays = get_connected_displays()
    if new_connected_displays != connected_displays:
        print('Display configuration changed.')
        # Configure the new displays using wlr-randr
        for display_name in new_connected_displays:
            if display_name not in connected_displays:
                configure_display(display_name)
        # Restart the Qtile session to apply the new display configuration
        restart_qtile()
        # Update the list of connected displays
        connected_displays = new_connected_displays

