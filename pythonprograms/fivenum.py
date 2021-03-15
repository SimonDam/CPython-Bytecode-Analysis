def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Fivenum#Python

from __future__ import division
import math
import sys
import random
 
def fivenum(array):
    n = len(array)
    if n == 0:
        print("you entered an empty array.")
        sys.exit()
    x = sorted(array)
 
    n4 = math.floor((n+3.0)/2.0)/2.0
    d = [1, n4, (n+1)/2, n+1-n4, n]
    sum_array = []
 
    for e in range(5):
        floor = int(math.floor(d[e] - 1))
        ceil = int(math.ceil(d[e] - 1))
        sum_array.append(0.5 * (x[floor] + x[ceil]))
 
    return sum_array

def print(*args, **kwargs):
    pass

random.seed(8734656424687684)
n = {n}
x = [(random.random()*2)-1 for _ in range(n)]
y = fivenum(x)
print(y)

"""
