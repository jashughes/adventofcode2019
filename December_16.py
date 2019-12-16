from math import ceil
from itertools import accumulate

with open("December_16_in.txt") as f:
    input_code = f.read()
inp = [int(x) for x in str(input_code)]

def multi(inlist, pattern):
    expan = pattern * (ceil(len(inlist)/(len(pattern))) + 1)
    out_list = [inlist[i] * expan[i + 1]  for i in range(len(inlist))]
    return(abs(sum(out_list)) % 10)

def get_pattern(el):
    patt = [0] * el + [1] * el + [0] * el + [-1] * el
    return(patt)

# part 1
for ph in range(100):
    new_input = []
    for d in range(len(inp)):
        new_input.append(multi(inp, get_pattern(d + 1)))
    inp = new_input
print(inp[0:8])

#part 2
full_inp  = inp * 10000
offset = int("".join([str(i) for i in inp[0:7]]))
inp = full_inp[(offset - 1):]


for ph in range(100):
    print(ph)
    inp.reverse()
    inp = list(accumulate(inp))
    inp.reverse()
    inp = [abs(x) % 10 for x in inp]
print(inp[1:9])

