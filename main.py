"""
Prints the scan code of all currently pressed keys.
Updates on every keyboard event.
"""
import sys
# sys.path.append('..')
import keyboard
from subprocess import getoutput

keymap = {}
with open('g513.csv') as f:
    for line in f:
        if line.strip() == '':
            continue
        k, v = line.strip().split(',')
        keymap[k] = v
print(keymap)

# def print_pressed_keys(e):
#     kp = keyboard._pressed_events
#     if kp:
#         print(' + '.join(str(code) for code in kp))
    
	
# keyboard.hook(print_pressed_keys)
# keyboard.wait()
