# Taken from: https://www.rosettacode.org/wiki/Ethiopian_multiplication#Python

tutor = True
 
def halve(x):
    return x // 2
 
def double(x):
    return x * 2
 
def even(x):
    return not x % 2
 
def ethiopian(multiplier, multiplicand):
    if tutor:
        print("Ethiopian multiplication of %i and %i" %
              (multiplier, multiplicand))
    result = 0
    while multiplier >= 1:
        if even(multiplier):
            if tutor:
                print("%4i %6i STRUCK" %
                      (multiplier, multiplicand))
        else:
            if tutor:
                print("%4i %6i KEPT" %
                      (multiplier, multiplicand))
            result += multiplicand
        multiplier   = halve(multiplier)
        multiplicand = double(multiplicand)
    if tutor:
        print()
    return result

def print(*args, **kwargs):
    pass

n = 2750
ethiopian(17**n, 34**n)

