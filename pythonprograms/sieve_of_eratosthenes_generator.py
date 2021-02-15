# Taken from: https://www.rosettacode.org/wiki/Sieve_of_Eratosthenes#Python

def iprimes_upto(limit):
    is_prime = [False] * 2 + [True] * (limit - 1)
    for n in range(int(limit**0.5 + 1.5)): # stop at ``sqrt(limit)``
        if is_prime[n]:
            for i in range(n * n, limit + 1, n): # start at ``n`` squared
                is_prime[i] = False
    for i in range(limit + 1):
        if is_prime[i]: yield i

def print(*args, **kwargs):
    pass

n = 50000000
print(list(iprimes_upto(n)))

