n = 6
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Find_palindromic_numbers_in_both_binary_and_ternary_bases#Python

from itertools import islice
 
digits = "0123456789abcdefghijklmnopqrstuvwxyz"
 
def baseN(num,b):
  if num == 0: return "0"
  result = ""
  while num != 0:
    num, d = divmod(num, b)
    result += digits[d]
  return result[::-1] # reverse
 
def pal2(num):
    if num == 0 or num == 1: return True
    based = bin(num)[2:]
    return based == based[::-1]
 
def pal_23():
    yield 0
    yield 1
    n = 1
    while True:
        n += 1
        b = baseN(n, 3)
        revb = b[::-1]
        #if len(b) > 12: break
        for trial in ('{{0}}{{1}}'.format(b, revb), '{{0}}0{{1}}'.format(b, revb),
                      '{{0}}1{{1}}'.format(b, revb), '{{0}}2{{1}}'.format(b, revb)):
            t = int(trial, 3)
            if pal2(t):
                yield t

def print(*args, **kwargs):
    pass

n = {n}
for pal23 in islice(pal_23(), n):
    print(pal23, baseN(pal23, 3), baseN(pal23, 2))

"""
