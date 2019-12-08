# Input dat
x, y = 25, 6   # problem definition
with open("December_8_image.txt") as f:
    img = f.read()
img = [int(x) for x in str(img)]

# Check each layer for number of 0s, 1s and 2s
zeroes = x * y # theoretical maximum
prod_1s_2s = 0
for l in range(0, len(img), x * y):
    lay = img[l:(l + x * y)]
    if lay.count(0) < zeroes:
        zeroes = lay.count(0)
        prod_1s_2s = lay.count(1) * lay.count(2)
print("part 1 data input validation check:", prod_1s_2s)

# Determine image
#    Take the first non-two value in the stack of layers. 
#    Then render that value as black (' ') or white ('#')
aes = {0: ' ', 1: '#'}
for px in range(x * y):
    rn = next(n for n in img[px::(x * y)] if n != 2)
    print(aes[rn], end = '' if px % x != x - 1 else '\n')