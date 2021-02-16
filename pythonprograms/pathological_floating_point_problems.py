n = 559
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Pathological_floating_point_problems#Python

from fractions import Fraction
 
def muller_seq(n:int) -> float:
    seq = [Fraction(0), Fraction(2), Fraction(-4)]
    for i in range(3, n+1):
        next_value = (111 - 1130/seq[i-1]
            + 3000/(seq[i-1]*seq[i-2]))
        seq.append(next_value)
    return float(seq[n])
 
import random

def print(*args, **kwargs):
    pass

random.seed(983458702346785)
n = {n}
 
for i in [3, 4, 5, 6, 7, 8, 20, 30, 50, 100] + [random.randint(1,n) for _ in range(n)]:
    print("{{:4d}} -> {{}}".format(i, muller_seq(i)))

"""
