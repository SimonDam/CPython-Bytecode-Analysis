# Taken from: https://www.rosettacode.org/wiki/Permutation_test#Python

from itertools import combinations as comb
 
def statistic(ab, a):
    sumab, suma = sum(ab), sum(a)
    return ( suma / len(a) -
             (sumab -suma) / (len(ab) - len(a)) )
 
def permutationTest(a, b):
    ab = a + b
    Tobs = statistic(ab, a)
    under = 0
    for count, perm in enumerate(comb(ab, len(a)), 1):
        if statistic(ab, perm) <= Tobs:
            under += 1
    return under * 100. / count


def print(*args, **kwargs):
    pass

import random
random.seed(928374983279384536987348)
n = 12
treatmentGroup = [random.randint(1,n) for _ in range(n)]
controlGroup   = [random.randint(1,n) for _ in range(n)]
under = permutationTest(treatmentGroup, controlGroup)
print("under=%.2f%%, over=%.2f%%" % (under, 100. - under))

