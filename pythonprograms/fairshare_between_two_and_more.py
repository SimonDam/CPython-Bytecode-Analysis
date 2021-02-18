def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Fairshare_between_two_and_more#Python

from itertools import count, islice
 
def _basechange_int(num, b):
    '''
    Return list of ints representing positive num in base b
 
    >>> b = 3
    >>> print(b, [_basechange_int(num, b) for num in range(11)])
    3 [[0], [1], [2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2], [1, 0, 0], [1, 0, 1]]
    >>>
    '''
    if num == 0:
        return [0]
    result = []
    while num != 0:
        num, d = divmod(num, b)
        result.append(d)
    return result[::-1]
 
def fairshare(b=2):
    for i in count():
        yield sum(_basechange_int(i, b)) % b

def print(*args, **kwargs):
    pass

n = {n}
if __name__ == '__main__':
    for b in range(2, n):
        print(f"{{b:>2}}: {{str(list(islice(fairshare(b), 25)))[1:-1]}}")

"""
