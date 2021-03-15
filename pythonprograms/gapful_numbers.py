def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Gapful_numbers#Python

from itertools import islice, count

def print(*args, **kwargs):
    pass

n = {n}
for start, b in [(100, 30), (1_000_000, 15), (1_000_000_000, 10), (1, n)]:
    print(f"\\nFirst {{b}} gapful numbers from {{start:_}}")
    print(list(islice(( x for x in count(start) 
                        if (x % (int(str(x)[0]) * 10 + (x % 10)) == 0) )
                      , b)))

"""
