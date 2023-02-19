"""
"Echo" pattern for G810 keyboard
requires keyboard module, which needs root access to hook into the keyboard
"""

# DISCLAIMER: I could not get the on_release event to work, so I had to use a loop to wait for the key to be released. this is NOT efficient, since when a key is held it basically spawns a bunch of threads that do nothing. I'm not sure how to fix this, but I'm sure there's a way.

# from pynput import keyboard
import keyboard
from time import sleep
from color_codes import colors, RGB
import subprocess
from sys import stderr
import threading

color1 = colors['blueviolet']
color2 = colors['darkorange']
fade = 5        # fade time in seconds
freq = 5        # animation frequency in Hz
g810_path = '/usr/bin/g810-led'


active = {}             # keys that are currently being animated
ignore = {272, 273, 274}  # ignore mouse keys
# map of `keyboard` keycodes to `g810-led` key names
keymap = {
    int(k): v for k, v in (line.strip().split(',')
                           for line in open('g513.csv')
                           if line.strip() != '')}


# buffer of current key colors, to prevent unnecessary calls to g810-led
keycache = {k: color1.hex_format() for k in keymap}


def update_key(key: int, color: str):
    if keycache[key] != color:
        keycache[key] = color
        subprocess.call([g810_path, '-k', keymap[key], color])


# set all keys to color1
subprocess.call([g810_path, '-a', color1.hex_format()])

# threaded function for animating active keys
def animate(key: int, event: threading.Event):
    def gradient(color1, color2, steps):
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        for i in range(steps):
            yield RGB(
                int(r1 + (r2 - r1) * i / steps),
                int(g1 + (g2 - g1) * i / steps),
                int(b1 + (b2 - b1) * i / steps)).hex_format()
    for grad in gradient(color2, color1, freq * fade):
        # if event is set, then the key has been pressed again, so stop animating
        if event.is_set():
            return
        update_key(key, grad)
        sleep(1/freq)
    # if the key is still active when the animation is done, remove it
    active.pop(key)


# yes there are hooks
# but there's a bug where you cant actually hook both presses and releases
# so this is the next best thing, sorry ryan this probably hurts to read
while True:
    event = keyboard.read_event()
    key = event.scan_code
    print(f"{key} {event.event_type} {event.name}")
    if key in keymap:
        # animate on release
        if event.event_type == 'up':
            active[key] = threading.Event()
            threading.Thread(target=animate, args=(key, active[key])).start()
        # set color on press, kill any active animations for this key
        elif event.event_type == 'down':
            if key in active:
                active[key].set()
            update_key(key, color2.hex_format())
        else:
            print('Unknown event type: ' + str(event.event_type), file=stderr)
    elif key in ignore:
        pass
    else:
        print('Unknown key code: ' + str(key), file=stderr)
