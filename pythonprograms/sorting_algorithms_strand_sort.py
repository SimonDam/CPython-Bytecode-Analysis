n = 26623
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Sorting_algorithms/Strand_sort#Python

def merge_list(a, b):
	out = []
	while len(a) and len(b):
		if a[0] < b[0]:
			out.append(a.pop(0))
		else:
			out.append(b.pop(0))
	out += a
	out += b
	return out
 
def strand(a):
	i, s = 0, [a.pop(0)]
	while i < len(a):
		if a[i] > s[-1]:
			s.append(a.pop(i))
		else:
			i += 1
	return s
 
def strand_sort(a):
	out = strand(a)
	while len(a):
		out = merge_list(out, strand(a))
	return out

n = {n}

def print(*args, **kwargs):
    pass

import random
random.seed(354456375546447)

print(strand_sort([random.randint(1, n) for _ in range(n)]))

"""
