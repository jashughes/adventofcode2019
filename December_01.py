
#At the first Go / No Go poll, every Elf is Go until the Fuel Counter-Upper. They haven't determined the amount of fuel required yet.

#Fuel required to launch a given module is based on its mass. 
# Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

#For example:

#    For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
#    For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
#    For a mass of 1969, the fuel required is 654.
#    For a mass of 100756, the fuel required is 33583.

#The Fuel Counter-Upper needs to know the total fuel requirement. 
# To find it, individually calculate the fuel needed for the mass of each module (your puzzle input), then add together all the fuel values.

#What is the sum of the fuel requirements for all of the modules on your spacecraft?

# Function to calculate fuel needs
def getFuelNeeds(mass):
    return(mass//3 -2)

# Read component masses
with open("component_masses.txt") as f:
    comps = f.readlines()

components = [int(x.rstrip("\n")) for x in comps]

# calculate fuel per component and sum
fuel = [getFuelNeeds(comp)for comp in components]
totFuel = sum(fuel)
print(totFuel)

# calculate fuel needs for fuel
fuel4fuel = 0
for fl in fuel:
    fl_needs = fl
    while fl_needs >= 0:
        fuel4fuel += fl_needs
        fl_needs = getFuelNeeds(fl_needs)

#Total fuel needs, including the fuel the fuel needs         
print(fuel4fuel)