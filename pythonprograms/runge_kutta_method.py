n = 327679
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Runge-Kutta_method#Python

def RK4(f):
    return lambda t, y, dt: (
            lambda dy1: (
            lambda dy2: (
            lambda dy3: (
            lambda dy4: (dy1 + 2*dy2 + 2*dy3 + dy4)/6
            )( dt * f( t + dt  , y + dy3   ) )
	    )( dt * f( t + dt/2, y + dy2/2 ) )
	    )( dt * f( t + dt/2, y + dy1/2 ) )
	    )( dt * f( t       , y         ) )
 
def theory(t): return (t**2 + 4)**2 /16
 
from math import sqrt

def print(*args, **kwargs):
    pass

n = {n}

dy = RK4(lambda t, y: t*sqrt(y))

t, y, dt = 0., 1., .1
while t <= n:
    if abs(round(t) - t) < 1e-5:
        print("y(%2.1f)\\t= %4.6f \\t error: %4.6g" % ( t, y, abs(y - theory(t))))
    t, y = t + dt, y + dy( t, y, dt )
 
 

"""
