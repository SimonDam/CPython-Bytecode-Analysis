n = 3135
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Hickerson_series_of_almost_integers#Python

from decimal import Decimal
import math
 
def h(n):
    'Simple, reduced precision calculation'
    return math.factorial(n) / (2 * math.log(2) ** (n + 1))
 
def h2(n):
    'Extended precision Hickerson function'
    return Decimal(math.factorial(n)) / (2 * Decimal(2).ln() ** (n + 1))

def print(*args, **kwargs):
    pass

n = {n}

for i in range(n):
    x = h2(i)
    norm = str(x.normalize())
    almostinteger = (' Nearly integer' 
                     if 'E' not in norm and ('.0' in norm or '.9' in norm) 
                     else ' NOT nearly integer!')
    print('n:%2i h:%s%s' % (i, norm, almostinteger))

"""
