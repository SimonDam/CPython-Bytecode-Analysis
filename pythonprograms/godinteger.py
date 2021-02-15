# Taken from: https://www.rosettacode.org/wiki/9_billion_names_of_God_the_integer#Python

cache = [[1]]
def cumu(n):
    for l in range(len(cache), n+1):
        r = [0]
        for x in range(1, l+1):
            r.append(r[-1] + cache[l-x][min(x, l-x)])
        cache.append(r)
    return cache[n]
 
def row(n):
    r = cumu(n)
    return [r[i+1] - r[i] for i in range(n)]
 
def print(*args, **kwargs):
    pass

print("rows:")
n = 10000
for x in range(1, n):
    print("%2d:"%x, row(x))

 
print("\nsums:")
for x in list(range(n)): 
    print(x, cumu(x)[-1])

