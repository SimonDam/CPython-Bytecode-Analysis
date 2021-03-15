def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Egyptian_division#Python

from itertools import product
 
def egyptian_divmod(dividend, divisor):
    assert divisor != 0
    pwrs, dbls = [1], [divisor]
    while dbls[-1] <= dividend:
        pwrs.append(pwrs[-1] * 2)
        dbls.append(pwrs[-1] * divisor)
    ans, accum = 0, 0
    for pwr, dbl in zip(pwrs[-2::-1], dbls[-2::-1]):
        if accum + dbl <= dividend:
            accum += dbl
            ans += pwr
    return ans, abs(accum - dividend)

def print(*args, **kwargs):
    pass

n = {n}
if __name__ == "__main__":
    # Test it gives the same results as the divmod built-in
    for i, j in product(range(13), range(1, 13)):
            assert egyptian_divmod(i, j) == divmod(i, j)
    
    
    # Mandated result
    i, j = 1574**n, 874**n
    print(f'{{i}} divided by {{j}} using the Egyption method is %i remainder %i' % egyptian_divmod(i, j))

"""
