def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Monty_Hall_problem#Python

import random
random.seed(98347598347598347958347958)
 #1 represents a car
 #0 represent a goat
 
stay = 0  #amount won if stay in the same position
switch = 0 # amount won if you switch 
 
n = {n}

def print(*args, **kwargs):
    pass

for i in range(n):
    lst = [1,0,0]           # one car and two goats
    random.shuffle(lst)     # shuffles the list randomly
 
    ran = random.randrange(3) # gets a random number for the random guess
 
    user = lst[ran] #storing the random guess 
 
    del(lst[ran]) # deleting the random guess
 
    huh = 0
    for i in lst: # getting a value 0 and deleting it
        if i ==0:
            del(lst[huh]) # deletes a goat when it finds it
            break
        huh+=1
 
    if user ==1: # if the original choice is 1 then stay adds 1
        stay+=1
 
    if lst[0] == 1: # if the switched value is 1 then switch adds 1
        switch+=1
 
print("Stay =",stay)
print("Switch = ",switch)
#Done by Sam Witton 09/04/2014

"""
