n = 1835007
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Digital_root#Python

def print(*args, **kwargs):
    pass

def digital_root (n):
    ap = 0
    n = abs(int(n))
    while n >= 10:
        n = sum(int(digit) for digit in str(n))
        ap += 1
    return ap, n

import random
random.seed(25314387634867458764398543685734875634)
n = {n}
 
if __name__ == '__main__':
    for t in [random.randint(1,n) for _ in range(n)]:
        persistance, root = digital_root(t)
        print("%12i has additive persistance %2i and digital root %i." 
              % (t, persistance, root))

"""
