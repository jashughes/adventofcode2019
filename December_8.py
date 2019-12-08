# Input dat
with open("December_8_image.txt") as f:
    img = f.read()
img = [int(x) for x in str(img)]


# Describe image: 25 px wide, 6 px tall
x, y = 25, 6
p = len(img) 

# Check each layer for number of 0s, 1s and 2s
zeroes = x * y # theoretical maximum
prod_1s_2s = 0
for l in range(0, p, x * y):
    lay = img[l:(l + x * y)]
    if lay.count(0) < zeroes:
        zeroes = lay.count(0)
        prod_1s_2s = lay.count(1) * lay.count(2)
print("part 1 data input validation check:", prod_1s_2s)


# Determine image
#    Take the first non-two value in the stack of layers, 
#    looping through each pixel in a layer
rendered = []
for px in range(x * y):
    rendered += [[x for x in img[px::(x * y)] if x != 2][0]]

for px in range(0, len(rendered), x):
    # print rendered image, switching out characters to display more attractively
    print(''.join([" " if x == 0 else "#" for x in rendered[px:(px + x)]]))

