n = 84
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Kronecker_product#Python

from itertools import (chain)
 
 
# kronecker :: [[a]] -> [[a]] -> [[a]]
def kronecker(m1, m2):
    return concatMap(
        lambda row2: concatMap(
            lambda elem2: [concatMap(
                lambda num2: concatMap(
                    lambda num1: [num1 * num2],
                    elem2
                ),
                m1[row2]
            )],
            m2
        ),
        range(len(m2))
    )
 
 
# concatMap :: (a -> [b]) -> [a] -> [b]
def concatMap(f, xs):
    return list(
        chain.from_iterable(
            map(f, xs)
        )
    )

import random
random.seed(983245798347659843769842369824756879425568972)

def print(*args, **kwargs):
    pass

n = {n}
if __name__ == '__main__':
    # Sample 1
    r = [[1, 2, 3], [3, 4]]
    s = [[0, 5], [6, 7]]
 
    # Sample 2
    t = [[random.randint(0,1) for _ in range(n)] for _ in range(n)]
    u = [[random.randint(0,1) for _ in range(n)] for _ in range(n)]
 
    # Result 1:
    for row in kronecker(r, s):
        print(row)
    print()
 
    # Result 2
    for row in kronecker(t, u):
        print(row)

"""
