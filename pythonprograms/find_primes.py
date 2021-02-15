# Written by Simon Dam Nielsen

def find_primes(start, end):
    primes = []
    for i in range(start, end):
        for j in range(2, (i//2)+1):
            if i % j == 0:
                break
        else:
            primes.append(i)
    return primes

n = 40000

if __name__ == "__main__":
    find_primes(1, n)


