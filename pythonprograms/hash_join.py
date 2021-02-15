# Taken from: https://www.rosettacode.org/wiki/Hash_join

from collections import defaultdict
 
def hashJoin(table1, index1, table2, index2):
    h = defaultdict(list)
    # hash phase
    for s in table1:
        h[s[index1]].append(s)
    # join phase
    return [(s, r) for r in table2 for s in h[r[index2]]]

import random
random.seed(38763489765283745283756)

def print(*args, **kwargs):
    pass

n = 500000
table1 = [(random.randint(1,int(n/10)), random.randint(1,int(n/10))) for _ in range(n)]
table2 = [(random.randint(1,int(n/10)), random.randint(1,int(n/10))) for _ in range(n)]
 
for row in hashJoin(table1, 1, table2, 0):
    print(row)

