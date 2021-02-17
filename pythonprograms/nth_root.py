n = 415055
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Nth_root#Python

from decimal import Decimal, getcontext
 
def nthroot (n, A, precision):
    getcontext().prec = precision
 
    n = Decimal(n)
    x_0 = A / n #step 1: make a while guess.
    x_1 = 1     #need it to exist before step 2
    while True:
        #step 2:
        x_0, x_1 = x_1, (1 / n)*((n - 1)*x_0 + (A / (x_0 ** (n - 1))))
        if x_0 == x_1:
            return x_1

n = {n}
nthroot(2, 5, n)

"""
