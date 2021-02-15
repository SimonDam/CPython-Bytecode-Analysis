# Taken from: https://www.rosettacode.org/wiki/Roots_of_a_function#Python

def print(*args, **kwargs):
    pass

n = 5000

f = lambda x: x * x * x - 3 * x * x + 2 * x
 
step = 0.001 # Smaller step values produce more accurate and precise results
start = -1
stop = n
 
sign = f(start) > 0
 
x = start
while x <= stop:
    value = f(x)
 
    if value == 0:
        # We hit a root
        print ("Root found at", x)
    elif (value > 0) != sign:
        # We passed a root
        print ("Root found near", x)
 
    # Update our sign
    sign = value > 0
 
    x += step

