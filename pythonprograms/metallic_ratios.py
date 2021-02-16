n = 4351
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Metallic_ratios#Python

from itertools import count, islice
from _pydecimal import getcontext, Decimal
 
def metallic_ratio(b):
    m, n = 1, 1
    while True:
        yield m, n
        m, n = m*b + n, m
 
def stable(b, prec):
    def to_decimal(b):
        for m,n in metallic_ratio(b):
            yield Decimal(m)/Decimal(n)
 
    getcontext().prec = prec
    last = 0
    for i,x in zip(count(), to_decimal(b)):
        if x == last:
            print(f'after {{i}} iterations:\\n\\t{{x}}')
            break
        last = x

def print(*args, **kwargs):
    pass

for b in range(4):
    coefs = [n for _,n in islice(metallic_ratio(b), 15)]
    print(f'\\nb = {{b}}: {{coefs}}')
    stable(b, 32)
 
print(f'\\nb = 1 with 256 digits:')
n = {n}
stable(1, n)

"""
