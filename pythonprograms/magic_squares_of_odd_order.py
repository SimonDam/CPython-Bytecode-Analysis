# Taken from: https://www.rosettacode.org/wiki/Magic_squares_of_odd_order#Python

def magic(n):
    for row in range(1, n + 1):
        print(' '.join('%*i' % (len(str(n**2)), cell) for cell in
                       (n * ((row + col - 1 + n // 2) % n) +
                       ((row + 2 * col - 2) % n) + 1
                       for col in range(1, n + 1))))
    print('\nAll sum to magic number %i' % ((n * n + 1) * n // 2))
 
def print(*args, **kwargs):
    pass

n = 2000
for i in (5, 3, 7, n):
	print('\nOrder %i\n=======' % i)
	magic(i)

