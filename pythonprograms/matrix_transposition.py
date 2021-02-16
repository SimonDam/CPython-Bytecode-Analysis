n = 2047
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Matrix_transposition#Python

# transpose :: Matrix a -> Matrix a
def transpose(m):
    if m:
        inner = type(m[0])
        z = zip(*m)
        return (type(m))(
            map(inner, z) if tuple != inner else z
        )
    else:
        return m

def print(*args, **kwargs):
    pass
 
import random
random.seed(2139847839857)
n = {n}

if __name__ == '__main__':
    # TRANSPOSING FOUR BASIC TYPES OF PYTHON MATRIX
    # Cartesian product of (Outer, Inner) with (List, Tuple)
 
    # Matrix any = Tuple of Tuples of any type
    tts = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
 
    # Matrix any = Tuple of Lists of any  type
    tls = ([1, 2, 3], [4, 5, 6], [7, 8, 9])
 
    emptyTuple = ()
 
    # Matrix any = List of Lists of any type
    lls = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
 
    # Matrix any = List of Tuples of any type
    lts = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    
    lst = [[random.random() for _ in range(n)] for _ in range(n)] 

    emptyList = []
 
    print('transpose function :: (Transposition without type change):\\n')
    for m in [emptyTuple, tts, tls, emptyList, lls, lts, lst]:
        tm = transpose(m)
        print (
            type(tm).__name__ + (
                (' of ' + type(tm[0]).__name__) if m else ''
            ) + ' :: ' + str(m) + ' -> ' + str(tm)
        )

"""
