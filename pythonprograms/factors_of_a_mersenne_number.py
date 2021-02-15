# Taken from: https://www.rosettacode.org/wiki/Factors_of_an_integer#Python

from math import sqrt

def factor(n):
      factors = set()
      for x in range(1, int(sqrt(n)) + 1):
        if n % x == 0:
          factors.add(x)
          factors.add(n//x)
      return sorted(factors)

n = 1000000000000000
factor(n)

