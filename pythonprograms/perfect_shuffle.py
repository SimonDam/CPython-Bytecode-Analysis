n = 2097152
min_n = 2
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Perfect_shuffle#Python

import doctest
import random
 
 
def flatten(lst):
    '''
    >>> flatten([[3,2],[1,2]])
    [3, 2, 1, 2]
    '''
    return [i for sublst in lst for i in sublst]
 
def magic_shuffle(deck):
    '''
    >>> magic_shuffle([1,2,3,4])
    [1, 3, 2, 4]
    '''
    half = len(deck) // 2 
    return flatten(zip(deck[:half], deck[half:]))
 
def after_how_many_is_equal(shuffle_type,start,end):
    '''
    >>> after_how_many_is_equal(magic_shuffle,[1,2,3,4],[1,2,3,4])
    2
    '''
 
    start = shuffle_type(start)
    counter = 1
    while start != end:
        start = shuffle_type(start)
        counter += 1
    return counter

def print(*args, **kwargs):
    pass

n = {n}

def main():
    doctest.testmod()
 
    print("Length of the deck of cards | Perfect shuffles needed to obtain the same deck back")
    for length in (8, 24, 52, n):
        deck = list(range(length))
        shuffles_needed = after_how_many_is_equal(magic_shuffle,deck,deck)
        print("{{}} | {{}}".format(length,shuffles_needed))
 
 
if __name__ == "__main__":
    main()
 

"""
