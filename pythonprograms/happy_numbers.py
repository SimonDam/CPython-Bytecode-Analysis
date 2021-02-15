# Taken from: https://www.rosettacode.org/wiki/Happy_numbers#Python

def happy(n):
    past = set()			
    while n != 1:
        n = sum(int(i)**2 for i in str(n))
        if n in past:
            return False
        past.add(n)
    return True

n = 300000
[x for x in range(n) if happy(x)][:n]


