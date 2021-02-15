# Taken from: https://www.rosettacode.org/wiki/Sorting_algorithms/Cocktail_sort#Python

def cocktailSort(A):
    up = range(len(A)-1)
    while True:
        for indices in (up, reversed(up)):
            swapped = False
            for i in indices:
                if A[i] > A[i+1]:  
                    A[i], A[i+1] =  A[i+1], A[i]
                    swapped = True
            if not swapped:
                return

import random
random.seed(6926928735872369856)

def print(*args, **kwargs):
    pass

n = 6000
test1 = [random.randint(1, n) for _ in range(n)]
cocktailSort(test1)
print(test1)


