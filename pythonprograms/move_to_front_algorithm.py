# Taken from: https://www.rosettacode.org/wiki/Move-to-front_algorithm#Python

from __future__ import print_function
from string import ascii_lowercase
import random
random.seed(92384739487594382398742)
 
SYMBOLTABLE = list(ascii_lowercase)
 
def move2front_encode(strng, symboltable):
    sequence, pad = [], symboltable[::]
    for char in strng:
        indx = pad.index(char)
        sequence.append(indx)
        pad = [pad.pop(indx)] + pad
    return sequence
 
def move2front_decode(sequence, symboltable):
    chars, pad = [], symboltable[::]
    for indx in sequence:
        char = pad[indx]
        chars.append(char)
        pad = [pad.pop(indx)] + pad
    return ''.join(chars)

def print(*args, **kwargs):
    pass

n = 3000000
if __name__ == '__main__':
    for s in ['broood', 'bananaaa', 'hiphophiphop', ''.join(random.choice(ascii_lowercase) for _ in range(n))]:
        encode = move2front_encode(s, SYMBOLTABLE)
        print('%14r encodes to %r' % (s, encode), end=', ')
        decode = move2front_decode(encode, SYMBOLTABLE)
        print('which decodes back to %r' % decode)
        assert s == decode, 'Whoops!'

