n = 2175
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Zig-zag_matrix#Python

def zigzag(n):
    '''zigzag rows'''
    def compare(xy):
        x, y = xy
        return (x + y, -y if (x + y) % 2 else y)
    xs = range(n)
    return {{index: n for n, index in enumerate(sorted(
        ((x, y) for x in xs for y in xs),
        key=compare
    ))}}
 
 
def printzz(myarray):
    '''show zigzag rows as lines'''
    n = int(len(myarray) ** 0.5 + 0.5)
    xs = range(n)
    print('\\n'.join(
        [''.join("%3i" % myarray[(x, y)] for x in xs) for y in xs]
    ))

def print(*args, **kwargs):
    pass

n = {n}
printzz(zigzag(n))

"""
