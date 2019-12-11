from itertools import permutations
from math import atan2
from math import sqrt

def find_asteroids(field):
    asteroids = []
    for y in range(len(field)):
        r = field[y]
        for x in range(len(r)):
            if r[x] == '#':
                asteroids += [(x, y)]
    return(asteroids)

def slope(t1, t2):
    return atan2(t1[0] - t2[0], t1[1] - t2[1])

# Set up objects
with open("December_10_input.txt") as f:
    field = f.readlines()
field = [x.rstrip("\n") for x in field]

ast = find_asteroids(field)

# PART ONE
# - for each asteroid, find the number of unique angles to each other asteroid.
d = {k: set() for k in ast}
for a, b in permutations(ast, 2):
    d[a].update([slope(a, b)])

max_asteroids = max([len(v) for v in d.values()])
loc = [k for k, v in d.items() if len(v) == max_asteroids][0]
print("Station should be built at", loc, "to be in range of ", max_asteroids, "asteroids")


# PART TWO:
# - find the distance and angle to each asteroid, store as a list of lists (easy to sort & access).
# - moving in clockwise in a circle from North, remove the nearest unblocked asteroid
# - i.e., skip asteroids for which the angle matches that of the previous asteroid
radar_map = []
for a in ast:
    ang = -slope(a, loc)
    dis = sqrt((a[1] - loc[1]) **2 + (a[0] - loc[0])** 2)
    radar_map += [[ang, dis, a[0], a[1]]]
radar_map = sorted(radar_map)

# Start the radar simulations
target_count = 0
angle = 360           #arbitrarily something not in radians.
while (len(radar_map) > 0 and target_count <= 200):
    for space_rock in radar_map:
        if space_rock[0] != angle:
            angle = space_rock[0]
            target_count += 1
            if target_count == 200:
                print("The 200th asteroid is", 100 * space_rock[2] + space_rock[3])
            radar_map.remove(space_rock)
            radar_map = sorted(radar_map)
