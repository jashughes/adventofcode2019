from math import ceil
from itertools import accumulate

with open("December_16_in.txt") as f:
    input_code = f.read()
inp = [int(x) for x in str(input_code)]

# A function to return the pattern [0, 1, 0, -1] with each element
# repeating "el" times
def get_pattern(el):
    patt = [0] * el + [1] * el + [0] * el + [-1] * el
    return(patt)

# A function to multiply an input list by the pattern (offset by 1 and 
# repeated to match at least the length of the input list)
def multi(inlist, pattern):
    expan = pattern * (ceil(len(inlist)/(len(pattern))) + 1)
    out_list = [inlist[i] * expan[i + 1]  for i in range(len(inlist))]
    return(abs(sum(out_list)) % 10)

# part 1
for ph in range(100):
    new_input = []
    for d in range(len(inp)):
        new_input.append(multi(inp, get_pattern(d + 1)))
    inp = new_input
print(inp[0:8])

#part 2
#   Generate input
inp = [int(x) for x in str(input_code)]
full_inp  = inp * 10000
#   Identify message offset
offset = int("".join([str(i) for i in inp[0:7]]))
#   Nothing prior to the offset contributes to our message due to the long number of leading zeros
#   Every other digit after the offset will be the `% 10` of the cumulative sum of subsquent digits
#   (All values multiplied by 1 - our offset is close to the end so dont need to worry about more 0 or negative numbers)
inp = full_inp[(offset - 1):]
inp.reverse()   # reverse it to make cumulative sum easier to calculate

for ph in range(100):
    print(ph)
    inp = [x % 10 for x in list(accumulate(inp))]
inp.reverse()    # reverse it again, since we've been working with our input backwards
print("our message is", "".join(str(x) for x in inp[1:9]))

