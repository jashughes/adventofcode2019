from itertools import product
import os

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
    triplet = []
    while mem["i"] < len(op):
        # Parse instructions
        op_code = op[mem["i"]] % 100
        inst = [int(x) for x in str(op[mem["i"]]).zfill(5)[:-2]]

        #Carry out task based on opcode using function specified in op_map
        op_map[op_code](mem, input_2, inst, op)

        if op_code == 99:
            break
        if len(mem["output_n"]) == 3:
            triplet = mem["output_n"]
            mem["output_n"] = []
            break
    return triplet

# A function to initiate the computer
def start_comp(amp_val, to_loop, intcode):
    return {"input_1": amp_val, "loop": to_loop, "i": 0, "in_counter": 0, "output_n": [], "rel": 0}, {k: v for k, v in enumerate(intcode)}

# A function to predict where the ball will intersect with the paddle
# probably a bit over-engineered...
def move_joy(b_old, b_new, H):
    if (b_old[0] == b_new[0]) and (H[0] == b_new[0]):
        return 0
    elif (b_old[0] == b_new[0]):
        return 1 if H[0] < b_new[0] else -1
    
    slo = (b_old[1] - b_new[1])/(b_old[0] - b_new[0])
    b = b_new[1] - slo * b_new[0]
    h_target = (H[1] - b)/slo

    if (H[0] == h_target):
        return 0
    else:
        return 1 if H[0] < h_target else -1

# A function to make the paddle follow the ball.
def track_ball(b_old, b_new, H):
    if b_new[0] == H[0]:
        return 0
    elif abs(b_new[1] - H[1]) < 2:
        return move_joy(b_old, b_new, H)
    elif b_new[0] < H[0]:
        return -1
    else:
        return 1

# A function to render a dictionary map
def render(di, aes):
    os.system('cls' if os.name == 'nt' else 'clear')
    xmax = max([k[0] for k in di.keys()])
    xmin = min([k[0] for k in di.keys()])
    ymax = max([k[1] for k in di.keys()])
    ymin = min([k[1] for k in di.keys()])
    
    for y in range(ymax + 1 + abs(ymin)):
        for x in range(xmax + 1 + abs(xmin)):
            color = di.get((x - abs(xmin), y - abs(ymin)), 0)
            print(aes[color], end = '')
        print()



# Read Input
with open("December_13_in.txt") as f:
    input_code = f.read()
input_code = [int(x) for x in input_code.split(",")]

# Initialize variables
input_code[0] = 2
joy = 0
mem, op = start_comp(joy, 1, input_code)
squares = {}
b_old, b_new = (15, 15), (15, 15) # rough location of start
H = (0, 0)
score = 0
aes = {0: ' ', 1: 'W', 2: ',', 3: 'H', 4: "O"}

while True:
    board = loop_mode(mem, joy, op)
    if len(board) < 3:
        break
    if board[0] == -1 and board[1] == 0:
        score = board[2]
    
    else:
        if board[2] == 3: # stick
            H = (board[0], board[1])

        if board[2] == 4: #ball
            b_old = b_new
            b_new = (board[0], board[1])
            joy = track_ball(b_old, b_new, H)
        squares[(board[0], board[1])] = board[2]

    # render image on ball/paddle movements
    if board[2] == 4 or board[2] == 3:
        render(squares, aes)
print(score)
