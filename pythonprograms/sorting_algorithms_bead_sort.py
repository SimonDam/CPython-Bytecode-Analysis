n = 12799
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Sorting_algorithms/Bead_sort#Python

import random
random.seed(65873487523469520)

#!/bin/python3
from itertools import zip_longest
 
# This is wrong, it works only on specific examples
def beadsort(l):
    return list(map(sum, zip_longest(*[[1] * e for e in l], fillvalue=0)))

def print(*args, **kwargs):
    pass

n = {n}

# Demonstration code:
print(beadsort([random.randint(1,n) for _ in range(n)]))

"""
