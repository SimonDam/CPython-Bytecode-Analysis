# Taken from: https://www.rosettacode.org/wiki/One_of_n_lines_in_a_file#Python

from random import randrange, seed
seed(1983475984370983780475098724558072458057425089756234)
try:
    range = xrange
except: pass
 
def one_of_n(lines): # lines is any iterable
    choice = None
    for i, line in enumerate(lines):
        if randrange(i+1) == 0:
            choice = line
    return choice
 
def one_of_n_test(n=10, trials=1000000):
    bins = [0] * n
    if n:
        for i in range(trials):
            bins[one_of_n(range(n))] += 1
    return bins

def print(*args, **kwargs):
    pass

n = 500000
print(one_of_n_test(trials=n))

