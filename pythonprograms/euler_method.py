def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Euler_method#Python

def euler(f,y0,a,b,h):
	t,y = a,y0
	while t <= b:
		print("%6.3f %6.3f" % (t,y))
		t += h
		y += h * f(t,y)
 
def newtoncooling(time, temp):
	return -0.07 * (temp - 20)

def print(*args, **kwargs):
    pass

n = {n}
euler(newtoncooling,10**300,0,n,10)
 

"""
