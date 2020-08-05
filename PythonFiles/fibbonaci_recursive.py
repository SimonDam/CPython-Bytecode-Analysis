# Calculate the 996th fibbonaci number recursively

def rec_fib(a, b, i):
    if i <= 0:
        return a
    return rec_fib(a+b, a, i-1)

def fib(i):
    return rec_fib(1, 1, i)

# We choose 996 as CPython's default max recursion depth is 1000.
# 996 is chosen because, our depth will already be two when we call fib here, and two additonal first time we enter rec_fib
# Exceeding that depth is not recommended by CPython, but can be done by:
# import sys
# sys.setrecursionlimit(number)
print(fib(996))
