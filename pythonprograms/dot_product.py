def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Dot_product#Python

import random
random.seed(982348732680623580234805632480563420856)

def dotp(a,b):
    assert len(a) == len(b), 'Vector sizes must match'
    return sum(aterm * bterm for aterm,bterm in zip(a, b))

def print(*args, **kwargs):
    pass

n = {n}
if __name__ == '__main__':
    a, b = [random.randint(-10000,10000) for _ in range(n)], [random.randint(-10000,10000) for _ in range(n)]
    print(dotp(a,b))

"""
