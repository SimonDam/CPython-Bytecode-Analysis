# Taken from: https://www.rosettacode.org/wiki/Sorting_algorithms/Merge_sort#Python

from heapq import merge
 
def merge_sort(m):
    if len(m) <= 1:
        return m
 
    middle = len(m) // 2
    left = m[:middle]
    right = m[middle:]
 
    left = merge_sort(left)
    right = merge_sort(right)
    return list(merge(left, right))

import random
random.seed(657834598756438976598432658723465897)

n = 500000
test = [random.randint(1, n) for _ in range(n)]
merge_sort(test)

