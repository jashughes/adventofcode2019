with open("December_22.txt") as f:
    input_code = f.readlines()

def cut_n(li, n):
    return(li[n:] + li[:n])

def deal_into_new(li):
    return(li[::-1])

def deal_w_increment(li, n):
    table = [0] * len(li)
    i = 0
    for c in li:
        table[i] = c
        i = (i + n) % len(li)
    return table

# Part 1:
deck = [x for x in range(10007)]

for row in input_code:
    print(row)
    if row[0:3] == "cut":
        deck = cut_n(deck, int(row[4:]))
    elif row[0:9] == "deal into":
        deck = deal_into_new(deck)
    elif row[0:9] == "deal with":
        deck = deal_w_increment(deck, int(row[20:]))

print(deck.index(2019))


# Part 2:
