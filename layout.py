# create a graph of the key layout, for reactive animations

# from keys import keymap
from itertools import product
from functools import cache


def layout(keep_blanks=False) -> dict:
    """
    - returns a dict of coordinates to keynames
    - dict is of the form {(x, y): keyname, ...}
    """

    # start by mapping out which key is in which coordinate
    coords = {}
    with open('layout.csv') as csvfile:
        for x, row in enumerate(csvfile.readlines()):
            for y, key in enumerate(row.split(',')):
                if key == '' and not keep_blanks:
                    continue
                coords[(x, y)] = key
    return coords


def distance_map(distance=1) -> dict:
    """
    - returns a dict of string keynames to a dict of adjacent keynames and their relative distance, up to `distance` away
    - distance=1 is the default, and returns a dict of adjacent keys
    - dict is of the form {keyname: {keyname: distance, ...}, ...}
    """

    # get the coordinates of each key
    coords = layout(keep_blanks=True)

    # define some helper functions for working with coordinates
    DIRS = tuple(set(product((-1, 0, 1), repeat=2)) - {(0, 0)})

    def add_coords(a, b):
        return (a[0] + b[0], a[1] + b[1])

    @cache
    def adjacent(coord: tuple) -> set:
        return {add_coords(coord, d) for d in DIRS}

    # create a dict of keynames to their coordinates using breadth-first search
    # first pass is just themselves
    keynames = {}
    # for each key on the keyboard
    for coord in coords:
        if coords[coord] == '':
            continue
        # for each distance pass
        adjmap = {coord: 0}
        queue = {coord}
        for dist in range(1, distance+1):
            if not queue:
                break
            nextpass = set()
            for k in queue:
                nextpass.update(adjacent(k))
            nextpass = nextpass.difference(adjmap).intersection(coords)
            adjmap.update(
                {k: dist for k in nextpass})
            queue = nextpass
        keynames[coords[coord]] = {coords[k]: d for k, d in adjmap.items() if coords[k] != ''}
    return keynames


if __name__ == '__main__':
    from time import time
    dist = 10
    start = time()
    distance_map(dist)
    print(
        f"Generation takes {round((time() - start) * 1000, 3)}ms for distance={dist}")
