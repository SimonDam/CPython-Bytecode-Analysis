# Taken from: https://www.rosettacode.org/wiki/Sorting_algorithms/Insertion_sort#Python

def insertion_sort(L):
    for i in range(1, len(L)):
        j = i-1 
        key = L[i]
        while (L[j] > key) and (j >= 0):
           L[j+1] = L[j]
           j -= 1
        L[j+1] = key

import random
random.seed(12346556479846987445)

n = 10000
test = [random.randint(1, n) for _ in range(n)]
insertion_sort(test)


