# Taken from: https://www.rosettacode.org/wiki/Faulhaber%27s_triangle#Python

'''Faulhaber's triangle'''
 
from itertools import (accumulate, chain, count, islice, starmap)
from fractions import (Fraction)
 
 
# faulhaberTriangle :: Int -> [[Fraction]]
def faulhaberTriangle(m):
    '''List of rows of Faulhaber fractions.'''
    def go(rs, n):
        xs = list(starmap(
            lambda x, y: Fraction(n, x) * y,
            zip(islice(count(2), m), rs)
        ))
        return [Fraction(1 - sum(xs), 1)] + xs
    return list(accumulate(
        [[]] + list(islice(count(0), 1 + m)),
        go
    ))[1:]
 
 
# faulhaberSum :: Integer -> Integer -> Integer
def faulhaberSum(p, n):
    '''Sum of the p-th powers of the first n
       positive integers.
    '''
    return sum(
        list(starmap(
            lambda x, y: y * (n ** x),
            zip(count(1), faulhaberTriangle(p)[-1])
        ))
    )
 
def print(*args, **kwargs):
    pass

# TEST ----------------------------------------------------
n = 500
def main():
    '''Tests'''
    fs = faulhaberTriangle(n)
    print(
        fTable(__doc__ + ':\n')(str)(
            compose(concat)(
                fmap(showRatio(3)(3))
            )
        )(
            index(fs)
        )(range(0, len(fs)))
    )
    print('')
    print(
        faulhaberSum(17, 1000)
    )
 
 
# DISPLAY -------------------------------------------------
 
# fTable :: String -> (a -> String) ->
#                     (b -> String) -> (a -> b) -> [a] -> String
def fTable(s):
    '''Heading -> x display function -> fx display function ->
                     f -> xs -> tabular string.
    '''
    def go(xShow, fxShow, f, xs):
        ys = [xShow(x) for x in xs]
        w = max(map(len, ys))
        return s + '\n' + '\n'.join(map(
            lambda x, y: y.rjust(w, ' ') + ' -> ' + fxShow(f(x)),
            xs, ys
        ))
    return lambda xShow: lambda fxShow: lambda f: lambda xs: go(
        xShow, fxShow, f, xs
    )
 
 
# GENERIC -------------------------------------------------
 
# compose (<<<) :: (b -> c) -> (a -> b) -> a -> c
def compose(g):
    '''Right to left function composition.'''
    return lambda f: lambda x: g(f(x))
 
 
# concat :: [[a]] -> [a]
# concat :: [String] -> String
def concat(xs):
    '''The concatenation of all the elements
       in a list or iterable.'''
    def f(ys):
        zs = list(chain(*ys))
        return ''.join(zs) if isinstance(ys[0], str) else zs
 
    return (
        f(xs) if isinstance(xs, list) else (
            chain.from_iterable(xs)
        )
    ) if xs else []
 
 
# fmap :: (a -> b) -> [a] -> [b]
def fmap(f):
    '''fmap over a list.
       f lifted to a function over a list.
    '''
    return lambda xs: list(map(f, xs))
 
 
# index (!!) :: [a] -> Int -> a
def index(xs):
    '''Item at given (zero-based) index.'''
    return lambda n: None if 0 > n else (
        xs[n] if (
            hasattr(xs, "__getitem__")
        ) else next(islice(xs, n, None))
    )
 
 
# showRatio :: Int -> Int -> Ratio -> String
def showRatio(m):
    '''Left and right aligned string
       representation of the ratio r.
    '''
    def go(n, r):
        d = r.denominator
        return str(r.numerator).rjust(m, ' ') + (
            ('/' + str(d).ljust(n, ' ')) if 1 != d else (
                ' ' * (1 + n)
            )
        )
    return lambda n: lambda r: go(n, r)
 
 
# MAIN ---
if __name__ == '__main__':
    main()

