# Taken from: https://www.rosettacode.org/wiki/Sorting_algorithms/Selection_sort#Python

def selection_sort(lst):
    for i, e in enumerate(lst):
        mn = min(range(i,len(lst)), key=lst.__getitem__)
        lst[i], lst[mn] = lst[mn], e
    return lst

n = 15000

import random
random.seed(5865643479864567986988576896978756)

a = [random.randint(1, n) for _ in range(n)]
a = selection_sort(a)

