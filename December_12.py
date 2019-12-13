from itertools import combinations
from operator import add

def gravity(moon1, moon2):
    dv1 = 0
    dv2 = 0

    if moon1 > moon2:
        dv1, dv2 = -1, 1
    elif moon1 < moon2:
        dv1, dv2 = 1, -1
    return dv1, dv2

def apply_gravity(positions, velocity):
    for moon1, moon2 in combinations(positions.keys(), 2):
        dv1, dv2 = gravity(positions[moon1], positions[moon2])
        velocity[moon1] = velocity[moon1] +  dv1
        velocity[moon2] = velocity[moon2] + dv2

def apply_velocity(positions, velocity):
    for moon in positions.keys():
        positions[moon] = velocity[moon] + positions[moon]

def energy(moon):
    return sum([abs(x) for x in moon])

def calculate_energy(positions, velocity):
    return sum([energy(positions[x]) * energy(velocity[x]) for x in positions.keys()]) 

# Get the prime factors of a number
def factors(n):
    result = []
    for i in range(2,n+1): 
        s = 0
        while n % i == 0:
            n = n/float(i)
            s += 1
        if s > 0:
            for k in range(s):
                result.append(i) 
    if n == 1:
        return result

# Find the lowest common denominator
def lcd(period):
    fx, fy, fz = factors(period[0]), factors(period[1]), factors(period[2])

    prod = 1
    for f in set(fx + fy + fz):
        prod = prod * (f ** max([fx.count(f), fy.count(f), fz.count(f)]))
    return(prod)

# Input
pos = {"io": [-7, -8, 9], "eur": [-12, -3, -4], "gan": [6, -17, -9], "cal": [4, -10, -6]}
vel = {"io": [0, 0, 0], "eur": [0, 0, 0], "gan": [0, 0, 0], "cal": [0, 0, 0]}

# Part 1 
# I broke this into doing each coordinate separately to address part 2
# I was a bit concerned about how much memory I might need to store and check
# the uniqueness of 3 dimensions of position/velocity, and only one coordinate
# needed to be checked at a time since they act independently!
for c in range(3):
    pc = {k:v[c] for k, v in pos.items()}
    vc =  {k:v[c] for k, v in vel.items()}
    for s in range(1000):
        apply_gravity(pc, vc)
        apply_velocity(pc, vc)
    for k in pos.keys():
        pos[k][c] = pc[k]
        vel[k][c] = vc[k]
print(calculate_energy(pos, vel))

# Part 2
# Find period at which each moon repeats
period = [0,0,0]
for c in range(3):
    new = True
    pc = {k:v[c] for k, v in pos.items()}
    vc =  {k:v[c] for k, v in vel.items()}
    steps = 0
    marked = {str(pc) + str(vc)}

    while new:
        apply_gravity(pc, vc)
        apply_velocity(pc, vc)
        steps +=1
        described = str(pc) + str(vc)
        new = described not in marked
        marked.add(described)
    period[c] = steps

# Find lowest common denominator
# period = [186028, 28482, 231614]
print(lcd(period))


    


