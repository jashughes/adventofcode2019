from fractions import Fraction
from itertools import permutations
from math import atan2
from math import sqrt

def find_asteroids(field):
    asteroids = []
    for y in range(len(field)):
        r = field[y]
        for x in range(len(r)):
            if r[x] == '#':
                asteroids += [tuple([x, y])]
    return(asteroids)

def slo(t1, t2):
    if t1[1] == t2[1]:
        return "V"
    return Fraction(t1[0] - t2[0], t1[1] - t2[1])

# Set up objects
with open("December_10_input.txt") as f:
    field = f.readlines()
field = [x.rstrip("\n") for x in field]

ast = find_asteroids(field)
ast = ast

# PART ONE
# d = {k: [set(), set()] for k in ast}
# for a, b in permutations(ast, 2):
#     fr = slo(a, b)
#     if a[0]> b[0]:
#         d[a][0].update([fr])
#     else:
#         d[a][1].update([fr])


# max_asteroids = max([len(v[0]) + len(v[1]) for v in d.values()]) + 1
# loc = [k for k, v in d.items() if len(v[0]) + len(v[1]) + 1 == max_asteroids]
loc = tuple([26, 36])
#print(loc, max_asteroids)

# PART TWO:
ang = {}
dis = {}
for a in ast:
    ang[a] = atan2(a[1] - loc[1], a[0] - loc[0])
    dis[a] = sqrt((a[1] - loc[1]) **2 + (a[0] - loc[0])** 2)

print(ang)




