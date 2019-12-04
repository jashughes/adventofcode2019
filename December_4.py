# Part 1
#########
#However, they do remember a few key facts about the password:

#    1 ) It is a six-digit number.
#    2) The value is within the range given in your puzzle input.
#    3) Two adjacent digits are the same (like 22 in 122345).
#    4) Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

# Part 2
##########

# An Elf just remembered one more important detail: 
#    5) the two adjacent matching digits are not part of a larger group of matching digits.

#How many different passwords within the range given in your puzzle input meet these criteria?

# Puzzle input
##############################################################################################
puzzle_input = [206938,679128]

# Define functions
##############################################################################################
from collections import Counter

# A function to check if a number occurs at least twice in sequence
def check_rule_3(ls):
    db = False
    b = 0
    while (not db) & (b < (len(ls) - 1)):
        db = (ls[b] == ls[b + 1])
        b += 1
    return(db)

# A function to check if the digits increase OR stay the same
def check_rule_4(lst):
    asc = True
    a = 0
    while asc & (a < (len(lst) - 1)):
        asc = lst[a] <= lst[a + 1]
        a += 1
    return(asc)

# Check if there is at least one number that occurs twice
# This rule is a little less elegant since it only holds provided rule 3 passes.
def check_rule_5_given_3(ls):
    c = Counter(ls)
    return(2 in c.values())


# Solve puzzle
##############################################################################################

# We don't need to check rule 1 and rule 2, 
# since they will always be true of the numbers in the puzzle input.

# Brute force check all numbers in the range for part 1
count_possibilities1 = 0
for n in range(puzzle_input[0], puzzle_input[1]):
    n_array = [int(d) for d in str(n)]
    r4 = check_rule_4(n_array)
    r3 = check_rule_3(n_array)
    if (r4 & r3):
        count_possibilities1 += 1

# Brute force check all numbers in the range for part 1
count_possibilities2 = 0
for n in range(puzzle_input[0], puzzle_input[1]):
    n_array = [int(d) for d in str(n)]
    r4 = check_rule_4(n_array)
    r3 = check_rule_3(n_array)
    r5 = check_rule_5_given_3(n_array)
    if (r4 & r3 & r5):
        count_possibilities2 += 1

print("The solution to part 1 is", count_possibilities1)
print("The solution to part 2 is", count_possibilities2)

