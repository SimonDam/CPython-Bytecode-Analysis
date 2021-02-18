def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Totient_function#Python

from math import gcd
 
def  φ(n):
    return sum(1 for k in range(1, n + 1) if gcd(n, k) == 1)

def print(*args, **kwargs):
    pass

n = {n}

if __name__ == '__main__':
    def is_prime(n):
        return φ(n) == n - 1
 
    for m in range(1, 26):
        print(f" φ({{m}}) == {{φ(m)}}{{', is prime' if is_prime(m)  else ''}}")
    count = 0
    for m in range(1, n + 1):
        count += is_prime(m)
        if m in {{100, 1000, 10_000}}:
            print(f"Primes up to {{m}}: {{count}}")

"""
