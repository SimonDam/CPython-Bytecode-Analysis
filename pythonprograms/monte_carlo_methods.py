n = 41943039
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Monte_Carlo_methods#Python

from random import random, seed
seed(923879834679834745983476983475987)

from math import hypot
try:
    import psyco
    psyco.full()
except:
    pass
 
def pi(nthrows):
    inside = 0
    for i in range(nthrows):
        if hypot(random(), random()) < 1:
            inside += 1
    return 4.0 * inside / nthrows

def print(*args, **kwargs):
    pass

n = {n}

for i in [10**4, 10**6, n]:
    print("%9d: %07f" % (i, pi(i)))

"""
