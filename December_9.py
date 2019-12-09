def par(mem, instr, whole_op, para):
    if instr == 1:
        return(para)
    elif instr == 2:
        return(whole_op[para + mem["rel"]])
    else:
        return(whole_op[para])

def add_inputs(mem, input_2, inst, op):
    op[op[mem["i"] + 3]] = par(mem, inst[2], op, op[mem["i"] + 1]) + par(mem, inst[1], op, op[mem["i"] + 2])
    mem["i"] += 4
def prod_inputs(mem, input_2, inst, op):
    op[op[mem["i"] + 3]] = par(mem, inst[2], op, op[mem["i"] + 1]) * par(mem, inst[1], op, op[mem["i"] + 2])
    mem["i"] += 4
def ins_input(mem, input_2, inst, op):
    op[op[mem["i"] + 1]] = mem["input_1"] if (mem["in_counter"] == 0) else input_2
    mem["in_counter"] += 1
    mem["i"] += 2
def fetch_output(mem, input_2, inst, op):
    mem["output_n"] = par(mem, inst[2], op, op[mem["i"] + 1])
    mem["i"] += 2
def jump_true(mem, input_2, inst, op):
    mem["i"] = par(mem, inst[1], op, op[mem["i"] + 2]) if (par(mem, inst[2], op, op[mem["i"] + 1]) != 0) else mem["i"] + 3
def jump_false(mem, input_2, inst, op):
    mem["i"] = par(mem, inst[1], op, op[mem["i"] + 2]) if (par(mem, inst[2], op, op[mem["i"] + 1]) == 0) else mem["i"] + 3
def less_than(mem, input_2, inst, op):
    op[op[mem["i"] + 3]] = int((par(mem, inst[2], op, op[mem["i"] + 1]) < par(mem, inst[1], op, op[mem["i"] + 2])))
    mem["i"] +=4
def equal_to(mem, input_2, inst, op):
    op[op[mem["i"] + 3]] = int((par(mem, inst[2], op, op[mem["i"] + 1]) == par(mem, inst[1], op, op[mem["i"] + 2])))
    mem["i"] +=4
def code_end(mem, input_2, inst, op):
    mem["loop"] = 0
def adjust_rel(mem, input_2, inst, op):
    mem["rel"] += par(mem, inst[2], op, op[mem["i"] + 1])
    mem["i"] += 2

def init_op_map():
    return({1: add_inputs, 2 : prod_inputs, 3 : ins_input, 4 : fetch_output, \
        5 : jump_true, 6 : jump_false, 7 : less_than, 8 : equal_to, 99: code_end, 9: adjust_rel})

def loop_mode(mem, input_2, op):
    op_map = init_op_map()
    while mem["i"] < len(op):
        # Parse instructions
        op_code = op[mem["i"]] % 100
        inst = [int(x) for x in str(op[mem["i"]]).zfill(5)[:-2]]
        print(inst, op_code)
        
        #Carry out task based on opcode using function specified in op_map
        op_map[op_code](mem, input_2, inst, op)

        print([mem[k] for k in mem.keys()])
        print([op[x] for x in op.keys() if x < 50])
        
        if op_code == 99:
            break
    return mem["output_n"]

def start_amp(amp_val, to_loop, intcode):
    return {"input_1": amp_val, "loop": to_loop, "i": 0, "in_counter": 0, "output_n": 0, "rel": 0}, l_to_d(intcode)

def l_to_d(op):
    d = {}
    for i in range(0, len(op)):
        d.update({i: op[i]})
    return(d)


with open("December_9_input.txt") as f:
    input_code = f.read()
input_code = [int(x) for x in input_code.split(",")]
input_code = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]


mem, op = start_amp(1, 0, input_code)
print(loop_mode(mem, 1, op))
print(input_code)