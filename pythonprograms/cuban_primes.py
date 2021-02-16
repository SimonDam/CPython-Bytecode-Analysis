n = 40959
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Cuban_primes#Python

import datetime
import math
 
def print(*args, **kwargs):
    pass

n = {n}

primes = [ 3, 5 ]
 
cutOff = 200
 
bigUn =  100_000
chunks = 50
little = bigUn / chunks
 
tn = " cuban prime"
print ("The first {{:,}}{{}}s:".format(cutOff, tn))
 
c = 0
showEach = True
u = 0
v = 1
st = datetime.datetime.now()

for i in range(1, n):
	found = False
	u += 6
	v += u
	mx = int(math.sqrt(v))
 
	for item in primes:
		if (item > mx):
			break
		if (v % item == 0):
			found = True
			break
 
	if (found == 0):
		c += 1
		if (showEach):
			z = primes[-1]
			while (z <= v - 2):
				z += 2
 
				fnd = False
				for item in primes:
					if (item > mx):
						break
					if (z % item == 0):
						fnd = True
						break
 
				if (not fnd):
					primes.append(z)
 
			primes.append(v)
			print("{{:>11,}}".format(v), end='')
 
			if (c % 10 == 0):
				print("");
			if (c == cutOff):
				showEach = False
				print ("Progress to the {{:,}}th {{}}:".format(bigUn, tn), end='')
		if (c % little == 0):
			print('.', end='')
		if (c == bigUn):
			break
 
print("");
print ("The {{:,}}th{{}} is {{:,}}".format(c, tn, v))
print("Computation time was {{}} seconds".format((datetime.datetime.now() - st).seconds))

"""
