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

def loop_mode(loop, i, in_counter, input_1, input_2, output_n, op):
    if loop == 0:
        return [loop, i, in_counter, input_1, input_2, output_n, op]
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
            loop = 0
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
            break
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
    return [loop, i, in_counter, output_n, op]

# initialize & loop
def start_amps(a, b, c, d, e):
    loop_a, loop_b, loop_c, loop_d, loop_e = 1, 1, 1, 1, 1
    i_a, i_b, i_c, i_d, i_e = 0, 0, 0, 0, 0
    in_counter_a, in_counter_b, in_counter_c, in_counter_d, in_counter_e = 0, 0, 0, 0, 0
    output_n_a, output_n_b, output_n_c, output_n_d, output_n_e = 0, 0, 0, 0, 0                         # change
    op_a, op_b, op_c, op_d, op_e = to_amp.copy(), to_amp.copy(), to_amp.copy(), to_amp.copy(), to_amp.copy()

    while (max([loop_a, loop_b, loop_c, loop_d, loop_e]) == 1):
        loop_a, i_a, in_counter_a, output_n_a, op_a = loop_mode(loop_a, i_a, in_counter_a, a, output_n_e, output_n_a, op_a)
        loop_b, i_b, in_counter_b, output_n_b, op_b = loop_mode(loop_b, i_b, in_counter_b, b, output_n_a, output_n_b, op_b)
        loop_c, i_c, in_counter_c, output_n_c, op_c = loop_mode(loop_c, i_c, in_counter_c, c, output_n_b, output_n_c, op_c)
        loop_d, i_d, in_counter_d, output_n_d, op_d = loop_mode(loop_d, i_d, in_counter_d, d, output_n_c, output_n_d, op_d)
        loop_e, i_e, in_counter_e, output_n_e, op_e = loop_mode(loop_e, i_e, in_counter_e, e, output_n_d, output_n_e, op_e)
    
    return output_n_e

# Try all combinations
sig  = 0
for A, B, C, D, E in permutations(range(5,10)):
    all_amp = start_amps(A, B, C, D, E)
    sig = max(all_amp, sig)
                    
print("part 2 signal is", sig)