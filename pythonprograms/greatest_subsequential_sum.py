def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Greatest_subsequential_sum#Python

def maxsumit(iterable):
    maxseq = seq = []
    start, end, sum_start = -1, -1, -1
    maxsum_, sum_ = 0, 0
    for i, x in enumerate(iterable):
        seq.append(x); sum_ += x
        if maxsum_ < sum_: 
            maxseq = seq; maxsum_ = sum_
            start, end = sum_start, i
        elif sum_ < 0:
            seq = []; sum_ = 0
            sum_start = i
    assert maxsum_ == sum(maxseq[:end - start])
    return maxseq[:end - start]

import random
random.seed(98437539862987346523984756837587234583724589273465)

n = {n}
def x ():
    for _ in range(n):
        yield random.randint(-10000,10000)

maxsumit(x())


"""
