import os
from random import randint

# A function to parse parameter mode and return index
def pari(mem, instr, offset, para):
    if instr == 1:
        return mem["i"] + offset
    elif instr == 2:
        return para + mem["rel"]
    else:
        return para

# A function to map instructions to the corresponding function
def init_op_map():
    return({1: add_inputs, 2 : prod_inputs, 3 : ins_input, 4 : fetch_output, \
        5 : jump_true, 6 : jump_false, 7 : less_than, 8 : equal_to, 99: code_end, 9: adjust_rel})
# 1
def add_inputs(mem, input_2, inst, op):
    op[pari(mem, inst[0], 3,  op[mem["i"] + 3])] = op.get(pari(mem, inst[2], 1, op[mem["i"] + 1]), 0) + op.get(pari(mem, inst[1], 2, op[mem["i"] + 2]), 0)
    mem["i"] += 4
#2
def prod_inputs(mem, input_2, inst, op):
    op[pari(mem, inst[0], 3,  op[mem["i"] + 3])] = op.get(pari(mem, inst[2], 1, op[mem["i"] + 1]), 0) * op.get(pari(mem, inst[1], 2, op[mem["i"] + 2]), 0)
    mem["i"] += 4
#3
def ins_input(mem, input_2, inst, op):
    op[pari(mem, inst[2], 1, op[mem["i"] + 1])] = mem["input_1"] if (mem["in_counter"] == 0) else input_2
    mem["in_counter"] += 1
    mem["i"] += 2
#4
def fetch_output(mem, input_2, inst, op):
    mem["output_n"] = op.get(pari(mem, inst[2], 1, op[mem["i"] + 1]), 0)
    mem["i"] += 2
#5
def jump_true(mem, input_2, inst, op):
    mem["i"] = op.get(pari(mem, inst[1], 2, op[mem["i"] + 2]), 0) if (op.get(pari(mem, inst[2], 1, op[mem["i"] + 1]), 0) != 0) else mem["i"] + 3
#6
def jump_false(mem, input_2, inst, op):
    mem["i"] = op.get(pari(mem, inst[1], 2, op[mem["i"] + 2]), 0) if (op.get(pari(mem, inst[2], 1, op[mem["i"] + 1]), 0) == 0) else mem["i"] + 3
#7
def less_than(mem, input_2, inst, op):
    op[pari(mem, inst[0], 3,  op[mem["i"] + 3])]  = int(op.get(pari(mem, inst[2], 1, op.get(mem["i"] + 1, 0)),0) < op.get(pari(mem, inst[1], 2, op.get(mem["i"] + 2, 0)), 0))
    mem["i"] +=4
#8
def equal_to(mem, input_2, inst, op):
    op[pari(mem, inst[0], 3,  op[mem["i"] + 3])]  = int(op.get(pari(mem, inst[2], 1, op.get(mem["i"] + 1, 0)),0) == op.get(pari(mem, inst[1], 2, op.get(mem["i"] + 2, 0)), 0))
    mem["i"] +=4
#99
def code_end(mem, input_2, inst, op):
    mem["loop"] = 0
#9
def adjust_rel(mem, input_2, inst, op):
    mem["rel"] += op.get(pari(mem, inst[2], 1, op[mem["i"] + 1]),0)
    mem["i"] += 2

# A function to iteratively parse the intcode, returning all outputs generated as an array.
def loop_mode(mem, input_2, op):
    op_map = init_op_map()
    while mem["i"] < len(op):
        # Parse instructions
        op_code = op[mem["i"]] % 100
        inst = [int(x) for x in str(op[mem["i"]]).zfill(5)[:-2]]

        #Carry out task based on opcode using function specified in op_map
        op_map[op_code](mem, input_2, inst, op)

        if op_code == 99 or op_code == 4:
            break
    return mem["output_n"]

# A function to initiate the computer
def start_comp(amp_val, to_loop, intcode):
    return {"input_1": amp_val, "loop": to_loop, "i": 0, "in_counter": 0, "output_n": [], "rel": 0}, {k: v for k, v in enumerate(intcode)}

# A function to render a dictionary map
def render(di, aes, pos):
    os.system('cls' if os.name == 'nt' else 'clear')
    xmax = max([k[0] for k in di.keys()])
    xmin = min([k[0] for k in di.keys()])
    ymax = max([k[1] for k in di.keys()])
    ymin = min([k[1] for k in di.keys()])
    
    for y in range(ymax + 1 + abs(ymin)):
        for x in range(xmax + 1 + abs(xmin)):
            color = di.get((x - abs(xmin), y - abs(ymin)), 3) if pos != (x - abs(xmin), y - abs(ymin)) else 4
            print(aes[color], end = '')
        print()

# A function to return the values of surrounding squares (3 = unknown)
def get_surroundings(p, di):
    N = di.get((p[0], p[1] + 1), 3)
    S = di.get((p[0], p[1] - 1), 3)
    W = di.get((p[0] - 1, p[1]), 3)
    E = di.get((p[0] + 1, p[1]), 3)
    return [N, S, W, E]

# a function to try moving the droid in a specified direction 
# and record the value, then return to the same position
def check_surroundings(o, p, di):
    val = loop_mode(mem, o + 1, op)
    di[dir_to_pos(o, pos)] = val
    if val != 0:
        val = loop_mode(mem, backwards(o), op)

# returns new position given old position and direction
def dir_to_pos(o, p):
    if o == 0:
        return (pos[0], p[1] + 1)
    if o == 1:
        return (pos[0], p[1] - 1)
    if o == 2:
        return (pos[0] - 1, p[1])
    if o == 3:
        return (pos[0] + 1, p[1])

# returns reverse direction of passed.
# note flip from 0-indexed to 1-indexed.
def backwards(o):
    if o == 1 or o == 3:
        return o
    else:
        return o + 2

#returns an intcode-ready direction given two position coordinates
def pos_to_dir(p_old, p_new):
    if p_new[1] > p_old[1]: # North
        return 1
    if p_new[1] < p_old[1]: # South
        return 2
    if p_new[0] > p_old[0]: # East
        return 4
    return 3                # West

# updates the traversal dictionary with the lowest number of steps 
# to get to that point
def traverse(steps, pos, tra):
    tra[pos] = min([tra.get(pos, steps), steps])
    return(tra[pos])

# Read Input
with open("December_15_in.txt") as f:
    input_code = f.read()
input_code = [int(x) for x in input_code.split(",")]

# initiate
mp = {(0,0): 1}
tra = {}     # dictionary of form {position: how we got there}
old_pos = (0, 0)
pos = (0,0)
aes = {0: 'WW', 1: '  ', 2: 'OO', 3: '__', 4: "@@"}
mem, op = start_comp(1, 1, input_code)
found = 1
steps = 0

while found != 2:
    opts = get_surroundings(pos, mp)
    # look at available options
    for o in range(4):
        if opts[o] == 3:
            check_surroundings(o, pos, mp)
    # plot
    render(mp, aes, pos)
    # decide where to move
    opts = get_surroundings(pos, mp)
    
    # if we found the oxygen, move there (for now):
    if 2 in opts:
        new_pos = dir_to_pos(opts.index(2), pos)
        steps = traverse(steps, new_pos, tra) + 1
        val = loop_mode(mem, opts.index(2) + 1, op)
        old_pos = pos
        pos = new_pos
        found = 2

    # for each spot, see if we have multiple options.
    # if we do, try to take unexplored routes.
    # if we don't have any unexplored areas, select one randomly.
    else:
        #if 1+ direction unexplored, take the first
        dir_opts = []
        for o in range(4):
            if opts[o] != 0:
                dir_opts.append(dir_to_pos(o, pos))
        # find an unexplored spot
        unexplored = [d for d in dir_opts if d not in tra.keys() and d != old_pos]
        if len(unexplored) == 0:
            # we have begun backtracing, take the position that isn't the old one.
            unexplored = [d for d in dir_opts if d != old_pos]
        if len(unexplored) == 0:       # then the only way back is backwards
            new_pos = old_pos
        else:                          #otherwise, randomly select a direction
            new_pos = unexplored[randint(0, len(unexplored) -1)]
        selected = pos_to_dir(pos, new_pos)
        steps = traverse(steps, new_pos, tra) + 1
        val = loop_mode(mem, selected, op)
        old_pos = pos
        pos = new_pos

print("Oxygen is at", new_pos)
print("Minimum number of steps is", tra[new_pos] +1)
print(max([v - (tra[new_pos]+ 1) for k, v in tra.items()]))

# part 2:
# same as before, but now we are finding the maximum of the direct routes starting from 
# the oxygen. We will loop for a set number of iterations to try make sure we hit 
# all the unexplored parts

# initiate
tra = {}     # dictionary of form {position: how we got there}
old_pos = (0, 0)
found = 0
steps = 0

while found < 10000:
    opts = get_surroundings(pos, mp)
    # look at available options
    for o in range(4):
        if opts[o] == 3:
            check_surroundings(o, pos, mp)
    # plot
    #render(mp, aes, pos)
    # decide where to move
    opts = get_surroundings(pos, mp)

    # for each spot, see if we have multiple options.
    # if we do, try to take unexplored routes.
    # if we don't have any unexplored areas, select one randomly.
    dir_opts = []
    for o in range(4):
        if opts[o] != 0:
            dir_opts.append(dir_to_pos(o, pos))
    # find an unexplored spot
    unexplored = [d for d in dir_opts if d not in tra.keys() and d != old_pos]
    if len(unexplored) == 0:
        # we have begun backtracing, take the position that isn't the old one.
        unexplored = [d for d in dir_opts if d != old_pos]
    if len(unexplored) == 0:       # then the only way back is backwards
        new_pos = old_pos
    else:                          #otherwise, randomly select a direction
        new_pos = unexplored[randint(0, len(unexplored) -1)]
    selected = pos_to_dir(pos, new_pos)
    steps = traverse(steps, new_pos, tra) + 1
    val = loop_mode(mem, selected, op)
    old_pos = pos
    pos = new_pos
    found += 1
    if found % 1000 == 0:
        print(found, ':', max([v for k, v in tra.items()]))

print("Maximum number of steps is", max([v for k, v in tra.items()]) + 1)

