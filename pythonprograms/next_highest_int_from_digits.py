n = 393215
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Next_highest_int_from_digits#Python

def closest_more_than(n, lst):
    "(index of) closest int from lst, to n that is also > n"
    large = max(lst) + 1
    return lst.index(min(lst, key=lambda x: (large if x <= n else x)))
 
def nexthigh(n):
    "Return nxt highest number from n's digits using scan & re-order"
    assert n == int(abs(n)), "n >= 0"
    this = list(int(digit) for digit in str(int(n)))[::-1]
    mx = this[0]
    for i, digit in enumerate(this[1:], 1):
        if digit < mx:
            mx_index = closest_more_than(digit, this[:i + 1])
            this[mx_index], this[i] = this[i], this[mx_index]
            this[:i] = sorted(this[:i], reverse=True)
            return int(''.join(str(d) for d in this[::-1]))
        elif digit > mx:
            mx, mx_index = digit, i
    return 0

import random
random.seed(23094832095843098)

def print(*args, **kwargs):
    pass


n = {n}
t = 10**n

if __name__ == '__main__':
    for x in [0, 9, 12, 21, 12453, 738440, 45072010, 95322020,
              9589776899767587796600, random.randint(t,t*10)]:
        print(f"{{x:>12_d}} -> {{nexthigh(x):>12_d}}")

"""
