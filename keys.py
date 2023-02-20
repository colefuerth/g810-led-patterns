import subprocess
from collections import defaultdict

g810_path = '/usr/bin/g810-led'

ignore = {272, 273, 274}
keymap = {
    int(k): v for k, v in (line.strip().split(',')
                           for line in open('g513.csv')
                           if line.strip() != '')}


def update_key(key: int, color: str, keycache=defaultdict(int)):
    # buffer of current key colors, to prevent unnecessary calls to g810-led
    if keycache[key] != color:
        keycache[key] = color
        subprocess.call([g810_path, '-k', keymap[key], color])