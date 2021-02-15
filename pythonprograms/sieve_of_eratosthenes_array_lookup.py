def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Sieve_of_Eratosthenes#Python

def primes_upto(limit):
    is_prime = [False] * 2 + [True] * (limit - 1) 
    for n in range(int(limit**0.5 + 1.5)): # stop at ``sqrt(limit)``
        if is_prime[n]:
            for i in range(n*n, limit+1, n):
                is_prime[i] = False
    return [i for i, prime in enumerate(is_prime) if prime]

def print(*args, **kwargs):
    pass

n = {n}
print(list(primes_upto(n)))

"""
