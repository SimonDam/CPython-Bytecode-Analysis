# Taken from: https://www.rosettacode.org/wiki/Sequence:_smallest_number_greater_than_previous_term_with_exactly_n_divisors#Python

def divisors(n):
    divs = [1]
    for ii in range(2, int(n ** 0.5) + 3):
        if n % ii == 0:
            divs.append(ii)
            divs.append(int(n / ii))
    divs.append(n)
    return list(set(divs))
 
 
def sequence(max_n=None):
    previous = 0
    n = 0
    while True:
        n += 1
        ii = previous
        if max_n is not None:
            if n > max_n:
                break
        while True:
            ii += 1
            if len(divisors(ii)) == n:
                yield ii
                previous = ii
                break

def print(*args, **kwargs):
    pass

n = 22
 
if __name__ == '__main__':
    for item in enumerate(sequence(n)):
        print(item)
 

