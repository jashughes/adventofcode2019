# Define problem
################################################################################
op_master = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,13,1,19,1,6,19,23,\
    2,6,23,27,1,5,27,31,2,31,9,35,1,35,5,39,1,39,5,43,1,43,10,47,2,\
        6,47,51,1,51,5,55,2,55,6,59,1,5,59,63,2,63,6,67,1,5,67,71,1,\
            71,6,75,2,75,10,79,1,79,5,83,2,83,6,87,1,87,5,91,2,9,91,95,\
                1,95,6,99,2,9,99,103,2,9,103,107,1,5,107,111,1,111,5,115,\
                    1,115,13,119,1,13,119,123,2,6,123,127,1,5,127,131,1,9,\
                        131,135,1,135,9,139,2,139,6,143,1,143,5,147,2,147,6,\
                            151,1,5,151,155,2,6,155,159,1,159,2,163,1,9,163,0,\
                                99,2,0,14,0]
target = 19690720

# Solution
################################################################################
#  a function to solve the intcode program
def test_op(op):
    for i in range(0, len(op), 4):
        if op[i] == 99:
            break
        elif op[i] != 1 and op[i] != 2:
            print("problem encountered at position ", i)
        elif op[i] == 1:
            op[op[i + 3]] = op[op[i + 1]] + op[op[i + 2]]

        elif op[i] == 2:
            op[op[i + 3]] = op[op[i + 1]] * op[op[i + 2]]
    
    return(op[0])

# a function to create the new intcode program with a given noun and verb
def create_new_op(op, noun, verb):
    new_op = [op[0], noun, verb] + op[3:]
    return(new_op)

# iterate through all combinations of nouns and verbs, and output the combination(s) that work
for noun in range(0,99):
    for verb in range(0,99):
        new_op = create_new_op(op_master, noun, verb)
        opstart = new_op[0:4]
        test_result = test_op(new_op)
        if test_result == target:
            print(noun * 100 + verb)

# part 1 answer: 10566835
# part 2 answer: 2347
