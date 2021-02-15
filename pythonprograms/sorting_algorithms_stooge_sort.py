# Taken from: https://www.rosettacode.org/wiki/Sorting_algorithms/Stooge_sort#Python

def stoogesort(L, i=0, j=None):
    if j is None:
        j = len(L) - 1
    if L[j] < L[i]:
        L[i], L[j] = L[j], L[i]
    if j - i > 1:
        t = (j - i + 1) // 3
        stoogesort(L, i  , j-t)
        stoogesort(L, i+t, j  )
        stoogesort(L, i  , j-t)
    return L
 
n = 500

import random
random.seed(879864345313458456987685164)

data = [random.randint(1, n) for _ in range(n)]
stoogesort(data)

