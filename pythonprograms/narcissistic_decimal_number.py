n = 24
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Narcissistic_decimal_number#Python

from __future__ import print_function
from itertools import count, islice
 
def narcissists():
    for digits in count(0):
        digitpowers = [i**digits for i in range(10)]
        for n in range(int(10**(digits-1)), 10**digits):
            div, digitpsum = n, 0
            while div:
                div, mod = divmod(div, 10)
                digitpsum += digitpowers[mod]
            if n == digitpsum:
                yield n

def print(*args, **kwargs):
    pass

n = {n}
for i, n in enumerate(islice(narcissists(), n), 1):
    print(n, end=' ')
    if i % 5 == 0: print() 
print()

"""
