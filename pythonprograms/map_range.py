n = 917503
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Mandelbrot_set#Python

def maprange( a, b, s):
    (a1, a2), (b1, b2) = a, b
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

from fractions import Fraction

def print(*args, **kwargs):
    pass

n = {n}

for s in range(n):
    print("%2g maps to %s" % (s, maprange( (0, 10), (-1, 0), Fraction(s))))


"""
