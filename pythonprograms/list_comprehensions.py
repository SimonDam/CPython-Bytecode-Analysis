# Taken from: https://www.rosettacode.org/wiki/List_comprehensions#Python

from functools import (reduce)
from operator import (add)
 
 
# pts :: Int -> [(Int, Int, Int)]
def pts(n):
    m = 1 + n
    return [(x, y, z) for x in range(1, m)
            for y in range(x, m)
            for z in range(y, m) if x**2 + y**2 == z**2]
 
 
# pts2 :: Int -> [(Int, Int, Int)]
def pts2(n):
    m = 1 + n
    return bindList(
        range(1, m)
    )(lambda x: bindList(
        range(x, m)
    )(lambda y: bindList(
        range(y, m)
    )(lambda z: [(x, y, z)] if x**2 + y**2 == z**2 else [])))
 
 
# pts3 :: Int -> [(Int, Int, Int)]
def pts3(n):
    m = 1 + n
    return concatMap(
        lambda x: concatMap(
            lambda y: concatMap(
                lambda z: [(x, y, z)] if x**2 + y**2 == z**2 else []
            )(range(y, m))
        )(range(x, m))
    )(range(1, m))
 
 
# GENERIC ---------------------------------------------------------
 
# concatMap :: (a -> [b]) -> [a] -> [b]
def concatMap(f):
    return lambda xs: (
        reduce(add, map(f, xs), [])
    )
 
 
# (flip concatMap)
# bindList :: [a] -> (a -> [b])  -> [b]
def bindList(xs):
    return lambda f: (
        reduce(add, map(f, xs), [])
    )
 
 
def main(n):
    for f in [pts, pts2, pts3]:
        print(f(n))

def print(*args, **kwargs):
    pass

n = 300
main(n)

