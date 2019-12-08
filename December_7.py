def test_op(op, input_1, input_2):
    i = 0
    output_n = 0
    in_counter = 0
    while i < len(op):
        # Parsing instructions
        if op[i] > 100:
            op_code = op[i] % 100
            par_instr = [int(x) for x in str(op[i])[:-2]]
            par_instr = [0] * (3-len(par_instr)) + par_instr
        else:
            op_code = op[i]
            par_instr = [0, 0, 0]
        # Program end, multiplication and addition instructions (from Day 2)
        if op_code == 99:
            break
        elif op_code == 1:
            op[op[i + 3]] = par_mode(par_instr[2], op, op[i + 1]) + par_mode(par_instr[1], op, op[i + 2])
            i += 4
        elif op_code == 2:
            op[op[i + 3]] = par_mode(par_instr[2], op, op[i + 1]) * par_mode(par_instr[1], op, op[i + 2])
            i += 4
        # Input/Output instructions
        elif op_code == 3:
            new_input = input_1 if (in_counter == 0) else input_2
            op[op[i + 1]] = new_input
            in_counter += 1
            i += 2
        elif op_code == 4:
            output_n = par_mode(par_instr[2], op, op[i + 1])
            i += 2
        # Jump if TRUE/Jump FALSE
        elif op_code == 5:
            if (par_mode(par_instr[2], op, op[i + 1]) != 0):
                i = par_mode(par_instr[1], op, op[i + 2])
            else:
                i += 3
        elif op_code == 6:
            if (par_mode(par_instr[2], op, op[i + 1]) == 0):
                i = par_mode(par_instr[1], op, op[i + 2])
            else:
                i += 3
        # Less than / Equal to
        elif op_code == 7:
            if (par_mode(par_instr[2], op, op[i + 1]) < par_mode(par_instr[1], op, op[i + 2])):
                op[op[i + 3]] = 1
            else:
                op[op[i + 3]] = 0
            i +=4
        elif op_code == 8:
            if (par_mode(par_instr[2], op, op[i + 1]) == par_mode(par_instr[1], op, op[i + 2])):
                op[op[i + 3]] = 1
            else:
                op[op[i + 3]] = 0
            i +=4
        # For error checking
        else:
            print("problem encountered at position ", i)
            break
    return(output_n)

# A function interpret parameter mode and return the appropriate value
def par_mode(instr, whole_op, para):
    if instr == 1:
        return(para)
    else:
        return(whole_op[para])


# Part 1
########################################################
to_amp = [3,8,1001,8,10,8,105,1,0,0,21,34,51,76,101,114,195,276,357,438,99999,3,9,1001,9,3,9,1002,9,3,9,4,9,99,3,9,101,4,9,9,102,4,9,9,1001,9,5,9,4,9,99,3,9,1002,9,4,9,101,3,9,9,102,5,9,9,1001,9,2,9,1002,9,2,9,4,9,99,3,9,1001,9,3,9,102,2,9,9,101,4,9,9,102,3,9,9,101,2,9,9,4,9,99,3,9,102,2,9,9,101,4,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99]
sig  = 0
for a in range(5):
    op = to_amp.copy()
    output_a = test_op(op, a, 0)
    for b in range(5):
        op = to_amp.copy()
        output_b = test_op(op, b, output_a)
        for c in range(5):
            op = to_amp.copy()
            output_c = test_op(op, c, output_b)
            for d in range(5):
                op = to_amp.copy()
                output_d = test_op(op, d, output_c)
                for e in range(5):
                    op = to_amp.copy()
                    output_e = test_op(op, e, output_d)

                    if (len(set([a, b, c, d, e])) == 5):
                        sig = max(output_e, sig)

print("max signal is", sig)


# Part 2
########################################################
from itertools import permutations

to_amp = [3,8,1001,8,10,8,105,1,0,0,21,34,51,76,101,114,195,276,357,438,99999,3,9,1001,9,3,9,1002,9,3,9,4,9,99,3,9,101,4,9,9,102,4,9,9,1001,9,5,9,4,9,99,3,9,1002,9,4,9,101,3,9,9,102,5,9,9,1001,9,2,9,1002,9,2,9,4,9,99,3,9,1001,9,3,9,102,2,9,9,101,4,9,9,102,3,9,9,101,2,9,9,4,9,99,3,9,102,2,9,9,101,4,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99]

def loop_mode(mem, input_2, op):
    if mem["loop"] == 0:
        return mem['output_n']
    while mem["i"] < len(op):
        # Parsing instructions
        if op[mem["i"]] > 100:
            op_code = op[mem["i"]] % 100
            par_instr = [int(x) for x in str(op[mem["i"]])[:-2]]
            par_instr = [0] * (3-len(par_instr)) + par_instr
        else:
            op_code = op[mem["i"]]
            par_instr = [0, 0, 0]
        # Program end, multiplication and addition instructions (from Day 2)
        if op_code == 99:
            mem["loop"] = 0
            break
        elif op_code == 1:
            op[op[mem["i"] + 3]] = par_mode(par_instr[2], op, op[mem["i"] + 1]) + par_mode(par_instr[1], op, op[mem["i"] + 2])
            mem["i"] += 4
        elif op_code == 2:
            op[op[mem["i"] + 3]] = par_mode(par_instr[2], op, op[mem["i"] + 1]) * par_mode(par_instr[1], op, op[mem["i"] + 2])
            mem["i"] += 4
        # Input/Output instructions
        elif op_code == 3:
            new_input = mem["input_1"] if (mem["in_counter"] == 0) else input_2
            op[op[mem["i"] + 1]] = new_input
            mem["in_counter"] += 1
            mem["i"] += 2
        elif op_code == 4:
            mem["output_n"] = par_mode(par_instr[2], op, op[mem["i"] + 1])
            mem["i"] += 2
            break
        # Jump if TRUE/Jump FALSE
        elif op_code == 5:
            if (par_mode(par_instr[2], op, op[mem["i"] + 1]) != 0):
                mem["i"] = par_mode(par_instr[1], op, op[mem["i"] + 2])
            else:
                mem["i"] += 3
        elif op_code == 6:
            if (par_mode(par_instr[2], op, op[mem["i"] + 1]) == 0):
                mem["i"] = par_mode(par_instr[1], op, op[mem["i"] + 2])
            else:
                mem["i"] += 3
        # Less than / Equal to
        elif op_code == 7:
            if (par_mode(par_instr[2], op, op[mem["i"] + 1]) < par_mode(par_instr[1], op, op[mem["i"] + 2])):
                op[op[mem["i"] + 3]] = 1
            else:
                op[op[mem["i"] + 3]] = 0
            mem["i"] +=4
        elif op_code == 8:
            if (par_mode(par_instr[2], op, op[mem["i"] + 1]) == par_mode(par_instr[1], op, op[mem["i"] + 2])):
                op[op[mem["i"] + 3]] = 1
            else:
                op[op[mem["i"] + 3]] = 0
            mem["i"] +=4
        # For error checking
        else:
            print("problem encountered at position ", mem["i"])
            break
    return mem["output_n"]

def start_amp(amp_val, intcode):
    return {"input_1": amp_val, "loop": 1, "i": 0, "in_counter": 0, "output_n": 0}, intcode.copy()
 
# initialize & loop
def run_amps(a, b, c, d, e):
    da, op_a = start_amp(a, to_amp)
    db, op_b = start_amp(b, to_amp)
    dc, op_c = start_amp(c, to_amp)
    dd, op_d = start_amp(d, to_amp)
    de, op_e = start_amp(e, to_amp)

    while (max([da["loop"], db["loop"], dc["loop"], dd["loop"], de["loop"]]) == 1):
        da["output_n"] = loop_mode(da, de["output_n"], op_a)
        db["output_n"] = loop_mode(db, da["output_n"], op_b)
        dc["output_n"] = loop_mode(dc, db["output_n"], op_c)
        dd["output_n"] = loop_mode(dd, dc["output_n"], op_d)
        de["output_n"] = loop_mode(de, dd["output_n"], op_e)
    
    return de["output_n"]


# Try all combinations
sig  = 0
for A, B, C, D, E in permutations(range(5,10)):
    all_amp = run_amps(A, B, C, D, E)
    sig = max(all_amp, sig)
                    
print("part 2 signal is", sig)