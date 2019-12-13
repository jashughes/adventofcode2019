from itertools import permutations
# A function interpret parameter mode and return the appropriate value
def par(instr, whole_op, para):
    if instr == 1:
        return(para)
    else:
        return(whole_op[para])

def add_inputs(mem, input_2, inst, op):
    op[op[mem["i"] + 3]] = par(inst[2], op, op[mem["i"] + 1]) + par(inst[1], op, op[mem["i"] + 2])
    mem["i"] += 4
def prod_inputs(mem, input_2, inst, op):
    op[op[mem["i"] + 3]] = par(inst[2], op, op[mem["i"] + 1]) * par(inst[1], op, op[mem["i"] + 2])
    mem["i"] += 4
def ins_input(mem, input_2, inst, op):
    op[op[mem["i"] + 1]] = mem["input_1"] if (mem["in_counter"] == 0) else input_2
    mem["in_counter"] += 1
    mem["i"] += 2
def fetch_output(mem, input_2, inst, op):
    mem["output_n"] = par(inst[2], op, op[mem["i"] + 1])
    mem["i"] += 2
def jump_true(mem, input_2, inst, op):
    mem["i"] = par(inst[1], op, op[mem["i"] + 2]) if (par(inst[2], op, op[mem["i"] + 1]) != 0) else mem["i"] + 3
def jump_false(mem, input_2, inst, op):
    mem["i"] = par(inst[1], op, op[mem["i"] + 2]) if (par(inst[2], op, op[mem["i"] + 1]) == 0) else mem["i"] + 3
def less_than(mem, input_2, inst, op):
    op[op[mem["i"] + 3]] = int((par(inst[2], op, op[mem["i"] + 1]) < par(inst[1], op, op[mem["i"] + 2])))
    mem["i"] +=4
def equal_to(mem, input_2, inst, op):
    op[op[mem["i"] + 3]] = int((par(inst[2], op, op[mem["i"] + 1]) == par(inst[1], op, op[mem["i"] + 2])))
    mem["i"] +=4
def code_end(mem, input_2, inst, op):
    mem["loop"] = 0

def init_op_map():
    return({1: add_inputs, 2 : prod_inputs, 3 : ins_input, 4 : fetch_output, \
        5 : jump_true, 6 : jump_false, 7 : less_than, 8 : equal_to, 99: code_end})

def loop_mode(mem, input_2, op):
    op_map = init_op_map()
    while mem["i"] < len(op):
        # Parse instructions
        op_code = op[mem["i"]] % 100
        inst = [int(x) for x in str(op[mem["i"]]).zfill(5)[:-2]]
        
        #Carry out task based on opcode using function specified in op_map
        op_map[op_code](mem, input_2, inst, op)
        if op_code in [4, 99]:
            break

    return mem["output_n"]

def start_amp(amp_val, to_loop, intcode):
    return {"input_1": amp_val, "loop": to_loop, "i": 0, "in_counter": 0, "output_n": 0}, intcode.copy()
 

def feedback_amps(a, b, c, d, e):
    da, op_a = start_amp(a, 1, to_amp)
    db, op_b = start_amp(b, 1, to_amp)
    dc, op_c = start_amp(c, 1, to_amp)
    dd, op_d = start_amp(d, 1, to_amp)
    de, op_e = start_amp(e, 1, to_amp)

    while (max([da["loop"], db["loop"], dc["loop"], dd["loop"], de["loop"]]) == 1):
        da["output_n"] = loop_mode(da, de["output_n"], op_a)
        db["output_n"] = loop_mode(db, da["output_n"], op_b)
        dc["output_n"] = loop_mode(dc, db["output_n"], op_c)
        dd["output_n"] = loop_mode(dd, dc["output_n"], op_d)
        de["output_n"] = loop_mode(de, dd["output_n"], op_e)
    
    return de["output_n"]

def series_amps(a, b, c, d, e):
    # Initialize amps
    da, op_a = start_amp(a, 0, to_amp)
    db, op_b = start_amp(b, 0, to_amp)
    dc, op_c = start_amp(c, 0, to_amp)
    dd, op_d = start_amp(d, 0, to_amp)
    de, op_e = start_amp(e, 0, to_amp)
    # Run amps
    da["output_n"] = loop_mode(da, 0, op_a)
    db["output_n"] = loop_mode(db, da["output_n"], op_b)
    dc["output_n"] = loop_mode(dc, db["output_n"], op_c)
    dd["output_n"] = loop_mode(dd, dc["output_n"], op_d)
    de["output_n"] = loop_mode(de, dd["output_n"], op_e)

    return de["output_n"]

# Load inputs & solve puzzle
with open("December_7_input.txt") as f:
    to_amp = f.read()
to_amp = [int(x) for x in to_amp.split(",")]

print("Part 1: max signal is", max(series_amps(*phases) for phases in permutations(range(5))))
print("Part 2: max signal is", max(feedback_amps(*phases) for phases in permutations(range(5,10))))