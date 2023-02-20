import subprocess
from collections import defaultdict

g810_path = '/usr/bin/g810-led'

ignore = {272, 273, 274}
keymap = {
    int(k): v for k, v in (line.strip().split(',')
                           for line in open('g513.csv')
                           if line.strip() != '')}

keymap_inv = {}
for k, v in keymap.items():
    if v in keymap_inv:
        k = min(k, keymap_inv[v])
    keymap_inv[v] = k


def update_key(key, color: str, keycache=defaultdict(int)):
    if isinstance(key, int):
        key = keymap[key]
    # buffer of current key colors, to prevent unnecessary calls to g810-led
    if keycache[key] != color:
        keycache[key] = color
        subprocess.call([g810_path, '-k', key, color])
