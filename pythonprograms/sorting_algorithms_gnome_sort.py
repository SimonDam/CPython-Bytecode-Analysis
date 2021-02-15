# Taken from: https://www.rosettacode.org/wiki/Sorting_algorithms/Gnome_sort#Python

def gnomesort(a):
    i,j,size = 1,2,len(a)
    while i < size:
        if a[i-1] <= a[i]:
            i,j = j, j+1
        else:
            a[i-1],a[i] = a[i],a[i-1]
            i -= 1
            if i == 0:
                i,j = j, j+1
    return a

import random
random.seed(5423863759875698767436)

n = 7000

gnomesort([random.randint(1, n) for _ in range(n)])


