n = 39
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Fibonacci_word#Python

import math
from collections import Counter

def entropy(s):
    p, lns = Counter(s), float(len(s))
    return -sum( count/lns * math.log(count/lns, 2) for count in p.values())


def fibword(nmax=37):
    fwords = ['1', '0']
    print('%-3s %10s %-10s %s' % tuple('N Length Entropy Fibword'.split()))
    def pr(n, fwords):
        while len(fwords) < n:
            fwords += [''.join(fwords[-2:][::-1])]
        v = fwords[n-1]
        print('%3i %10i %10.7g %s' % (n, len(v), entropy(v), v if len(v) < 20 else '<too long>'))
    for n in range(1, nmax+1): pr(n, fwords)

def print(*args, **kwargs):
    pass

n = {n}
fibword(n)

"""
