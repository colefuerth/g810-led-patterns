#!/usr/bin/python3
"""
"Echo" pattern for G810 keyboard
requires keyboard module, which needs root access to hook into the keyboard
"""

import keyboard
from time import sleep
from color_codes import colors, RGB
import subprocess
from sys import stderr
import threading

color1 = colors['blueviolet']
color2 = colors['darkorange']
fade = 8         # fade time in seconds
freq = 10        # animation frequency in Hz
g810_path = '/usr/bin/g810-led'


active = {}
ignore = {272, 273, 274}
keymap = {
    int(k): v for k, v in (line.strip().split(',')
                           for line in open('g513.csv')
                           if line.strip() != '')}


def update_key(key: int, color: str, keycache={k: color1.hex_format() for k in keymap}):
    # buffer of current key colors, to prevent unnecessary calls to g810-led
    if keycache[key] != color:
        keycache[key] = color
        subprocess.call([g810_path, '-k', keymap[key], color])


# set all keys to color1
subprocess.call([g810_path, '-a', color1.hex_format()])


def animate(key: int, event: threading.Event, effect='gradient'):
    # threaded function for animating active keys
    # event is used to stop animations in progress if the key is pressed again
    if effect == 'gradient':
        def gradient(color1, color2, steps):
            r1, g1, b1 = color1
            r2, g2, b2 = color2
            for i in range(steps):
                yield RGB(
                    int(r1 + (r2 - r1) * i / steps),
                    int(g1 + (g2 - g1) * i / steps),
                    int(b1 + (b2 - b1) * i / steps)).hex_format()
        for grad in gradient(color2, color1, freq * fade):
            if event.is_set():
                return
            update_key(key, grad)
            sleep(1/freq)
    else:
        raise ValueError('Unknown effect: ' + effect)


def on_event(event):
    key = event.scan_code
    if key in keymap:
        # animate on release
        if event.event_type == 'up':
            e = threading.Event()
            threading.Thread(target=animate, args=(key, e)).start()
            if key in active:
                active[key].set()
            active[key] = e
        # set color on press, kill any active animations for this key
        elif event.event_type == 'down':
            if key in active:
                active[key].set()
                active.pop(key)
            update_key(key, color2.hex_format())
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
