n = 46
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Loops/Increment_loop_index_within_loop_body#Python

def isPrime(n):
    for x in 2, 3:
        if not n % x:
            return n == x
    d = 5
    while d * d <= n:
        for x in 2, 4:
            if not n % d:
                return False
            d += x
    return True

def print(*args, **kwargs):
    pass

n = {n}
 
i = 42
a = 0
while a < n:
    if isPrime(i):
        a += 1
        print('n = {{:2}} {{:20,}}'.format(a, i))
        i += i - 1
    i += 1

"""
