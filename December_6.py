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
# The approach here is to make a new dictionary of "hops" to COM for both YOU and SAN.
# The minimum hop count will be the minimum value of the sum of hops for YOU to that fork and SAN to that fork.

# Get orbit hop counts for YOU
d_you = {}
val = orbd["YOU"]
hops = 0
while val != 'COM':
    d_you.update({val: hops})
    val = orbd[val]
    hops += 1

# Get orbit hop counts for SAN
d_san = {}
val = orbd["SAN"]
hops = 0
while val != 'COM':
    d_san.update({val: hops})
    val = orbd[val]
    hops += 1

common = d_you.keys() & d_san.keys()
hop_totals = [d_san[k] + d_you[k] for k in common]

print("minimum hops to Santa is", min(hop_totals))

