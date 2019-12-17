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

        if op_code == 99:
            break
    return mem["output_n"]

# A function to initiate the computer
def start_comp(to_loop, intcode):
    return {"loop": to_loop, "i": 0, "in_counter": 0, "output_n": [], "rel": 0}, {k: v for k, v in enumerate(intcode)}

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

# A function to return the values of surrounding squares and self (0 = unknown)
def get_surroundings(p, di):
    N = di.get((p[0], p[1] + 1), 0)
    S = di.get((p[0], p[1] - 1), 0)
    W = di.get((p[0] - 1, p[1]), 0)
    E = di.get((p[0] + 1, p[1]), 0)
    M = di.get((p[0], p[1]), 0)
    return [N, S, W, E, M]

# A function to render a list map
def renderl(li):
    os.system('cls' if os.name == 'nt' else 'clear')
    for x in range(len(li)):
        print(chr(li[x]), end = '')

# A function to render a dictionary map
def renderd(di):
    #os.system('cls' if os.name == 'nt' else 'clear')
    xmax = max([k[0] for k in di.keys()])
    xmin = min([k[0] for k in di.keys()])
    ymax = max([k[1] for k in di.keys()])
    ymin = min([k[1] for k in di.keys()])
    
    for y in range(ymax + 1 + abs(ymin)):
        for x in range(xmax + 1 + abs(xmin)):
            color = di.get((x - abs(xmin), y - abs(ymin)), 3)
            print(chr(color), end = '')
        print()



# Read Input
with open("December_17_in.txt") as f:
    input_code = f.read()
input_code = [int(x) for x in input_code.split(",")]

# Initialize intcode
mem, op = start_comp(0, input_code)
img = loop_mode(mem, 1, op)

#renderl(img)

# Turn input into more useful format...
x, y = 0, 0
dimg = {}
for i in range(len(img) - 1):
    if img[i] != 10:
        dimg[(x, y)] = img[i]
        x += 1
    else:
        y += 1
        x = 0

# Part 1: Check for intersections
cs = 0
for k in dimg.keys():
    if set(get_surroundings(k, dimg)) == {35}:
        cs += k[0] * k[1]
print(cs)


# Part 2
L = 76
R = 82
man = [L, 12, L, 12, L, 6, L, 6, 
    # A
       R, 8, R, 4, L, 12,       
    # B
       L, 12, L, 12, L, 6, L, 6, 
    # A
       L, 12, L, 6, R, 12, R, 8, 
    # C
       R, 8, R, 4, L, 12,        
    # B
       L, 12, L, 12, L, 6, L, 6, 
    # A
       L, 12, L, 6, R, 12, R, 8, 
    # C
       R, 8, R, 4, L, 12,        
    # B
       L, 12, L, 12, L, 6, L, 6, 
    # A
       L, 12, L, 6, R, 12, R, 8]
    # C

A = "L,12,L,12,L,6,L,6\n"
B = "R,8,R,4,L,12\n"
C = "L,12,L,6,R,12,R,8\n"

mp = "A,B,A,C,B,A,C,B,A,C\n"
bot = "n\n"
command_s = mp + A + B + C + bot
command_n = [ord(x) for x in command_s]


# Send input to bot
input_code[0] = 2
mem, op = start_comp(1, input_code)

out = loop_mode(mem, command_n, op)
print(out[-1])