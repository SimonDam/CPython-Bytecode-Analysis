def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Count_in_factors#Python

from functools import lru_cache
 
primes = [2, 3, 5, 7, 11, 13, 17]    # Will be extended
 
@lru_cache(maxsize=2000)
def pfactor(n):
    if n == 1:
        return [1]
    n2 = n // 2 + 1
    for p in primes:
        if p <= n2:
            d, m = divmod(n, p)
            if m == 0:
                if d > 1:
                    return [p] + pfactor(d)
                else:
                    return [p]
        else:
            if n > primes[-1]:
                primes.append(n)
            return [n]

def print(*args, **kwargs):
    pass

n = {n}
if __name__ == '__main__':
    for i in range(1, n + 1):
        factors = pfactor(i)
        if i <= 10 or i >= i - 20:
            print( '%4i %5s %s' % (i,
                                   '' if factors != [i] or i == 1 else 'prime',
                                   'x'.join(str(i) for i in factors)) )
        if i == 11:
            print('...')
 
    print('\\nNumber of primes gathered up to', i, 'is', len(primes))
    print(pfactor.cache_info())

"""
