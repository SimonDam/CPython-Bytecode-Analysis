def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Pierpont_primes#Python

import random
 
# Copied from https://rosettacode.org/wiki/Miller-Rabin_primality_test#Python
def is_Prime(n):
    '''
    Miller-Rabin primality test.
 
    A return value of False means n is certainly not prime. A return value of
    True means n is very likely a prime.
    '''
    if n!=int(n):
        return False
    n=int(n)
    #Miller-Rabin test for prime
    if n==0 or n==1 or n==4 or n==6 or n==8 or n==9:
        return False
 
    if n==2 or n==3 or n==5 or n==7:
        return True
    s = 0
    d = n-1
    while d%2==0:
        d>>=1
        s+=1
    assert(2**s * d == n-1)
 
    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True  
 
    for i in range(8):#number of trials 
        a = random.randrange(2, n)
        if trial_composite(a):
            return False
 
    return True
 
def pierpont(ulim, vlim, first):
    p = 0
    p2 = 1
    p3 = 1
    pp = []
    for v in range(vlim):
        for u in range(ulim):
            p = p2 * p3
            if first:
                p = p + 1
            else:
                p = p - 1
            if is_Prime(p):
                pp.append(p)
            p2 = p2 * 2
        p3 = p3 * 3
        p2 = 1
    pp.sort()
    return pp

def print(*args, **kwargs):
    pass

random.seed(834587029346587234658702345873248756)
n = {n}
def main():
    print( "First 50 Pierpont primes of the first kind:")
    pp = pierpont(2, 40, True)
    for i in range(len(pp)):
        print( "%8d " % pp[i],)
        if (i - 9) % 10 == 0:
            print()
    print( "First 50 Pierpont primes of the second kind:")
    pp2 = pierpont(n, 80, False)
    for i in range(len(pp2)):
        print( "%8d " % pp2[i],)
        if (i - 9) % 10 == 0:
            print()
    print( "250th Pierpont prime of the first kind:", pp[1])
    print( "250th Pierpont prime of the second kind:", pp2[1])
 
main()

"""
