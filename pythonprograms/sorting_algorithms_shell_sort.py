# Taken from: https://www.rosettacode.org/wiki/Sorting_algorithms/Shell_sort#Python

def shell(seq):
    inc = len(seq) // 2
    while inc:
        for i, el in enumerate(seq[inc:], inc):
            while i >= inc and seq[i - inc] > el:
                seq[i] = seq[i - inc]
                i -= inc
            seq[i] = el
        inc = 1 if inc == 2 else inc * 5 // 11

n = 500000

import random
random.seed(154215616545476865488967489664)

a = [random.randint(1, n) for _ in range(n)]
a = shell(a)

