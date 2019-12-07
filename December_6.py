# Load data, store as a dictionary.
#    I will use the orbiting object as the key, 
#    and the orbit center as the value
with open("orbits.txt") as f:
    orbits = f.readlines()
orbits = [x.rstrip("\n").split(")") for x in orbits]
orbits = [t[::-1] for t in orbits]
orbd = dict(orbits)

# Part 1
#####################################
# approach is to calculate "hops" to COM for each orbiter.
n_orbs = 0
for key in orbd.keys():
    val = orbd[key]
    n_orbs += 1
    while val != 'COM':
        val = orbd[val]
        n_orbs += 1

print("n orbits is", n_orbs)

# Part 2
#####################################
# The approach here is to make a new dictionary of "hops" for you to travel to COM. (I.e., {"PLANET": hops}) 
# Then we will walk backwards from SAN to the first common planet for SAN and YOU, counting the hops for SAN to this planet.

# Get orbit hop counts for YOU
d_you = {}
val = orbd["YOU"]
hops = 0
while val != 'COM':
    d_you.update({val: hops})
    val = orbd[val]
    hops += 1

# Count hops for SAN to first branch in common with YOU.
val = orbd["SAN"]
hops = 0
while val not in d_you:
    val = orbd[val]
    hops += 1

print("minimum hops to Santa is", hops + d_you[val])

