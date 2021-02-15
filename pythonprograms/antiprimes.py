def source_code(n):	
    return f"""#Taken from: https://www.rosettacode.org/wiki/Anti-primes#Python
from itertools import chain, count, cycle, islice, accumulate
 
def factors(n):
    def prime_powers(n):
        for c in accumulate(chain([2, 1, 2], cycle([2,4]))):
            if c*c > n: break
            if n%c: continue
            d,p = (), c
            while not n%c:
                n,p,d = n//c, p*c, d + (p,)
            yield(d)
        if n > 1: yield((n,))
 
    r = [1]
    for e in prime_powers(n):
        r += [a*b for a in r for b in e]
    return r
 
def antiprimes():
    mx = 0
    for c in count(1):
        ln = len(factors(c))
        if ln > mx:
            yield c
            mx = ln        

def print(*args, **kwargs):
    pass

n = {n}

if __name__ == '__main__':
    print(list(islice(antiprimes(), n)))

"""
