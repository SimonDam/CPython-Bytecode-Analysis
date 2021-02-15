# Taken from: https://www.rosettacode.org/wiki/Fibonacci_sequence#Python

def fib(n,x=[0,1]):
   for i in range(abs(n)-1): x=[x[1],sum(x)]
   return x[1]*pow(-1,abs(n)-1) if n<0 else x[1] if n else 0

def print(*args, **kwargs):
    pass

n = 3000
for i in range(-n,n+1): print(fib(i))

