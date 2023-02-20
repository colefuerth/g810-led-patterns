#!/usr/bin/python3
"""
"Echo" pattern for G810 keyboard
requires keyboard module, which needs root access to hook into the keyboard
"""

# BUGGY, DO NOT USE

import keyboard
from time import sleep
from color_codes import colors, RGB
import subprocess
from sys import stderr
import threading
from keys import *
import layout

# SETTINGS

color1 = colors['blueviolet']
color2 = colors['darkorange']
fade = 6         # fade time in seconds
freq = 10        # animation frequency in Hz
dist = 1         # distance from each key to animate
step = 3         # inverse scale by which each distance is multiplied, ex step=2 means 1, 1/2, 1/4 brightness, etc

# END SETTINGS

active = {}
keylayout = layout.distance_map(dist)
subprocess.call([g810_path, '-a', color1.hex_format()])


def gradient(color1, color2, weight: float):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return RGB(
        int(r1 + (r2 - r1) * weight),
        int(g1 + (g2 - g1) * weight),
        int(b1 + (b2 - b1) * weight)).hex_format()


def animation(key: str, event: threading.Event):
    # threaded function for animating active keys
    # event is used to stop animations in progress if the key is pressed again

    while active[key][1] > 0:
        update_key(key, gradient(color1, color2, active[key][1]))
        active[key][1] -= 1 / (fade * freq)
        sleep(1/freq)
        if event.is_set():
            break
    update_key(key, color1.hex_format())
    if key in active and active[key][0] == event:
        active.pop(key)


def on_event(event):
    key = event.scan_code
    if key in keymap:
        key = keymap[key]
        # animate on release
        if event.event_type == 'up':
            active[key] = [threading.Event(), 1]
            threading.Thread(target=animation, args=(
                key, active[key][0])).start()
        # set color on press, kill any active animations for this key
        elif event.event_type == 'down':
            # set current key
            if key in active:
                active[key][0].set()
            update_key(key, color2.hex_format())
            # animate adjacent keys
            for k, d in keylayout[key].items():
                if d == 0 or keyboard.is_pressed(keymap_inv[k]):
                    continue
                if k in active:
                    active[k][1] = min(active[k][1] + 1/d, 1)
                    continue
                active[k] = [threading.Event(), 1/d]
                threading.Thread(target=animation, args=(
                    k, active[k][0])).start()
        else:
            print('Unknown event type: ' + str(event.event_type), file=stderr)
    elif key in ignore:
        pass
    else:
        print('Unknown key code: ' + str(key), file=stderr)


if __name__ == '__main__':
    # asynchronously handle keyboard events because it trips up when I type too fast otherwise
    while True:
        event = keyboard.read_event()
        threading.Thread(target=on_event, args=(event,)).start()
