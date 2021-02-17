n = 1151
min_n = 1
def source_code(n):	
    return f"""#Taken from: https://www.rosettacode.org/wiki/Abundant_odd_numbers#Python

#!/usr/bin/python
# Abundant odd numbers - Python
def print(*args, **kwargs):
    pass

n = {n}
 
oddNumber  = 1
aCount  = 0
dSum  = 0
 
from math import sqrt
 
def divisorSum(n):
    sum = 1
    i = int(sqrt(n)+1)
 
    for d in range (2, i):
        if n % d == 0:
            sum += d
            otherD = n // d
            if otherD != d:
                sum += otherD
    return sum
 
print ("The first 25 abundant odd numbers:")
while aCount  < 25:
    dSum  = divisorSum(oddNumber )
    if dSum  > oddNumber :
        aCount  += 1
        print("{{0:5}} proper divisor sum: {{1}}". format(oddNumber ,dSum ))
    oddNumber  += 2
 
while aCount  < n:
    dSum  = divisorSum(oddNumber )
    if dSum  > oddNumber :
        aCount  += 1
    oddNumber  += 2
print ("\\n1000th abundant odd number:")
print ("    ",(oddNumber - 2)," proper divisor sum: ",dSum)
 
oddNumber  = 10 + 1
found  = False
while not found :
    dSum  = divisorSum(oddNumber )
    if dSum  > oddNumber :
        found  = True
        print ("\\nFirst abundant odd number > 1 000 000 000:")
        print ("    ",oddNumber," proper divisor sum: ",dSum)
    oddNumber  += 2

"""
