# Taken from: https://www.rosettacode.org/wiki/Topswops#Python

from itertools import permutations
def f1(p):
    i = 0
    while True:
        p0  = p[0]
        if p0 == 1: break
        p[:p0] = p[:p0][::-1]
        i  += 1
    return i
 
def fannkuch(n):
    return max(f1(list(p)) for p in permutations(range(1, n+1)))
 
def print(*args, **kwargs):
    pass
 
n = 11

for i in range(1, n):
    print(i,fannkuch(i))

