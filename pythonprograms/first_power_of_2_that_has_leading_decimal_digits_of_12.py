def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/First_power_of_2_that_has_leading_decimal_digits_of_12#Python

from math import log, modf, floor
 
def p(l, n, pwr=2):
    l = int(abs(l))
    digitcount = floor(log(l, 10))
    log10pwr = log(pwr, 10)
    raised, found = -1, 0
    while found < n:
        raised += 1
        firstdigits = floor(10**(modf(log10pwr * raised)[0] + digitcount))
        if firstdigits == l:
            found += 1
    return raised

def print(*args, **kwargs):
    pass
 
import random
random.seed(213445769348654687)
n = {n}
if __name__ == '__main__':
    for l, n in ((x, y) for x, y in zip(range(1, n+1), range(1, n+1))):
        print(f"p({{l}}, {{n}}) =", p(l, n))

"""
