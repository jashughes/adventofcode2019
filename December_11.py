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
    op[pari(mem, inst[2], 1, op[mem["i"] + 1])] = mem["input_1"] if (mem["in_counter"] == 0) else input_2
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
    paint_code = []
    while mem["i"] < len(op):
        # Parse instructions
        op_code = op[mem["i"]] % 100
        inst = [int(x) for x in str(op[mem["i"]]).zfill(5)[:-2]]

        #Carry out task based on opcode using function specified in op_map
        op_map[op_code](mem, input_2, inst, op)

        if op_code == 99:
            break
        if len(mem["output_n"]) == 2:
            paint_code = mem["output_n"]
            mem["output_n"] = []
            break
    return paint_code

# A function to initiate the computer
def start_comp(amp_val, to_loop, intcode):
    return {"input_1": amp_val, "loop": to_loop, "i": 0, "in_counter": 0, "output_n": [], "rel": 0}, {k: v for k, v in enumerate(intcode)}

# A function to change the direction vector
def directions(dir, turn):
    if turn == 0:
        return [dir[1], -dir[0]]
    return [-dir[1], dir[0]]

# a function to update the robot location
def move(coords, dir):
    return coords[0] + dir[0], coords[1] + dir[1]

# Read Input
with open("December_11_input.txt") as f:
    input_code = f.read()
input_code = [int(x) for x in input_code.split(",")]

# initiate computate
floor_color = 1 # problem statement
paint_mem, paint_op = start_comp(floor_color, 1, input_code)
di = [0, 1] # start facing up
co = (0, 0) # start at 0,0
squares_seen = {(0,0): 1}  # start at 0, 0, which is black
while paint_mem["loop"] == 1:
    paint_instr = loop_mode(paint_mem, floor_color, paint_op)
    if (len(paint_instr)!= 2):
        break
    floor_color = paint_instr[0]
    squares_seen[co] = floor_color                 # add square/color to record "paint"
    di = directions(di, paint_instr[1])            # turn
    co = move(co, di)                              # move
    floor_color = squares_seen.get(co, 0)          # read new color
    if (paint_mem["loop"] == 0):
        break

print("Squares the painter covers:", len(squares_seen.keys())) #1930

# Render the image
aes = {0: ' ', 1: '#'}
xmin = min([k[0] for k in squares_seen.keys()])
xmax = max([k[0] for k in squares_seen.keys()])
ymin = min([k[1] for k in squares_seen.keys()])
ymax = max([k[1] for k in squares_seen.keys()])


painting = [[0] * (-xmin + 1)] * (-ymin)

for y in range(-ymin + 1):
    for x in range(-xmin):
        color = squares_seen.get((-x, -y), 0)
        print(aes[color], end = '')
    print()

#for r in painting:
#    print(''.join([aes[c] for c in r]))
#
#print(squares_seen.get((0,-1), 0), squares_seen.get((0,-2), 0), squares_seen.get((-1,-1), 0), squares_seen.get((-1,-2), 0))










