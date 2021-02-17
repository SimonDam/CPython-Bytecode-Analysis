n = 720895
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Sorting_algorithms/Comb_sort#Python

def combsort(input):
    gap = len(input)
    swaps = True
    while gap > 1 or swaps:
        gap = max(1, int(gap / 1.25))  # minimum gap is 1
        swaps = False
        for i in range(len(input) - gap):
            j = i+gap
            if input[i] > input[j]:
                input[i], input[j] = input[j], input[i]
                swaps = True

import random
random.seed(32584848684307567894305)

n = {n}
y = [random.randint(1, n) for _ in range(n)]
combsort(y)
assert y == sorted(y)

"""
