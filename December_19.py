import os
from itertools import product

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
    op[pari(mem, inst[2], 1, op[mem["i"] + 1])] = input_2[mem["in_counter"]]
    mem["in_counter"] += 1
    mem["i"] += 2
#4
def fetch_output(mem, input_2, inst, op):
    mem["output_n"].append(op.get(pari(mem, inst[2], 1, op[mem["i"] + 1]), 0))
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
def start_comp(to_loop, intcode):
    return {"loop": to_loop, "i": 0, "in_counter": 0, "output_n": [], "rel": 0}, {k: v for k, v in enumerate(intcode)}

# A function to render a dictionary map
def renderd(di, aes):
    #os.system('cls' if os.name == 'nt' else 'clear')
    xmax = max([k[0] for k in di.keys()])
    ymax = max([k[1] for k in di.keys()])
    
    for y in range(ymax + 1):
        for x in range(xmax + 1):
            color = di.get((x, y), 0)
            #print(color)
            print(aes[color], end = '')
        print()

# A function that returns True if Santa cant fit in the beam
# And false if he could fit in the beam
def check_no_santa(X, Y, di, dis):
    if di.get((X - dis, Y), 0) !=1:
        return True
    elif di.get((X, Y - dis), 0) !=1:
        return True
    elif di.get((X - dis, Y - dis), 0) !=1:
        return True
    else:
        return False


# Read Input
with open("December_19.txt") as f:
    input_code = f.read()
input_code = [int(x) for x in input_code.split(",")]

#PART 1
# Loop through coordinates to see if tractor beam
beam = {}
aes = {0: " ", 1: "#"}
for x, y in product(range(50), range(50)):
    mem, op = start_comp(0, input_code)
    beam[(x, y)] = loop_mode(mem, [x, y], op)[-1]
renderd(beam, aes)
print(sum([v for k, v in beam.items()]))

# PART 2
# Iterate close to the beam for efficiency.
# check the four corners of the 100 x 100 square.
beam = {(0,0): 1}
ds = 100 - 1
no_santa = True
x, y = 0, 0
xmi = 0
aes = {0: " ", 1: "#"}

while no_santa:
    last_x = 0
    in_beam = True
    #renderd(beam, aes)
    while in_beam:
        mem, op = start_comp(0, input_code)
        outp = loop_mode(mem, [x, y], op)[-1]
        beam[(x, y)] = outp

        # check if we can fit santa in the beam
        no_santa = check_no_santa(x, y, beam, ds)
        if not no_santa:
            print(10000 * (x - ds) + (y - ds))
            break

        # check if we have found the beam
        if last_x == 0 and outp == 1:
            xmi = x

        # check if we have left the beam
        last_x = max(last_x, outp)
        if last_x == 1 and outp == 0:
            y += 1
            x = xmi
            in_beam = False
        else:
            x += 1




    