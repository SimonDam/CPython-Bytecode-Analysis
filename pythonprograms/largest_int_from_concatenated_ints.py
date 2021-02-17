n = 1048575
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Largest_int_from_concatenated_ints#Python

try:
    cmp     # Python 2 OK or NameError in Python 3
    def maxnum(x):
        return ''.join(sorted((str(n) for n in x),
                              cmp=lambda x,y:cmp(y+x, x+y)))
except NameError:
    # Python 3
    from functools import cmp_to_key
    def cmp(x, y):
        return -1 if x<y else ( 0 if x==y else 1)
    def maxnum(x):
        return ''.join(sorted((str(n) for n in x),
                              key=cmp_to_key(lambda x,y:cmp(y+x, x+y))))

import random

def print(*args, **kwargs):
    pass

random.seed(82346508274563087245608274653)
n = {n}
for numbers in [(1, 34, 3, 98, 9, 76, 45, 4), (54, 546, 548, 60), tuple([random.randint(1,1000000) for _ in range(n)])]:
    print('Numbers: %r\\n  Largest integer: %15s' % (numbers, maxnum(numbers)))

"""
