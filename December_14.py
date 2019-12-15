from math import ceil
from math import floor

# Process Input
with open("December_14_test.txt") as f:
    rxns = f.readlines()
rxns = [l.rstrip("\n").split("=>") for l in rxns]

dr = {'ORE': [1, [1], ["ORE"]]}
for e in rxns:
    prod = e[1].split()
    rt = e[0].split()
    dr[prod[1]] = [int(prod[0]), [int(r) for r in rt[0::2]], [r.replace(",", "") for r in rt[1::2]]]

#print(dr)

needs = {}
new_needs = {'FUEL': 1}
excess = {}
ore = 0

#while [k for k in new_needs.keys()] != ['ORE']:
while len(new_needs.keys()) > 0:
    needs = {k:v for k, v in new_needs.copy().items() if v != 0}
    new_needs = {}
    for reagent in needs.keys():
        # Find quantity of each new_reagent needed to produce reagent
        new_reagents = dr[reagent][2]
        quantities = dr[reagent][1]
        stoich = ceil(needs[reagent] / dr[reagent][0])
        for nr in range(len(new_reagents)):
            if (new_reagents[nr]) == 'ORE':
                ore += stoich * quantities[nr]
            else: 
                new_needs[new_reagents[nr]] =  stoich * quantities[nr] + new_needs.get(new_reagents[nr], 0)
                # Check if we still have some we can use
                if (new_reagents[nr]) in excess.keys():
                    if excess[new_reagents[nr]] >= new_needs[new_reagents[nr]]:
                        excess[new_reagents[nr]] -= new_needs[new_reagents[nr]]
                        new_needs[new_reagents[nr]] = 0
                    else: 
                        new_needs[new_reagents[nr]] -= excess[new_reagents[nr]]
                        excess[new_reagents[nr]] = 0

        excess[reagent] = stoich * dr[reagent][0] - needs[reagent] + excess.get(reagent, 0)

# clean-up
for k in excess.keys():
    if dr[k][0] <= excess[k]:
        ore -= floor(excess[k]/dr[k][0]) * dr[k][1][0]
        excess[k] -= floor(excess[k]/dr[k][0]) * dr[k][0]

print(ore)
print(excess)

