# Taken from: https://www.rosettacode.org/wiki/Knuth%27s_power_tree#Python

from __future__ import print_function
 
# remember the tree generation state and expand on demand
def path(n, p = {1:0}, lvl=[[1]]):
	if not n: return []
	while n not in p:
		q = []
		for x,y in ((x, x+y) for x in lvl[0] for y in path(x) if not x+y in p):
			p[y] = x
			q.append(y)
		lvl[0] = q
 
	return path(p[n]) + [n]
 
def tree_pow(x, n):
    r, p = {0:1, 1:x}, 0
    for i in path(n):
        r[i] = r[i-p] * r[p]
        p = i
    return r[n]
 
def show_pow(x, n):
    fmt = "%d: %s\n" + ["%g^%d = %f", "%d^%d = %d"][x==int(x)] + "\n"
    print(fmt % (n, repr(path(n)), x, n, tree_pow(x, n)))

def print(*args, **kwargs):
    pass

n = 20000

for x in range(n): show_pow(2, x)
show_pow(3, 191)
show_pow(1.1, 81)
