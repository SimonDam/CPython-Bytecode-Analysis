# Taken from: https://www.rosettacode.org/wiki/One-dimensional_cellular_automata#Python

import random
random.seed(239847908375298374598347598374)

def print(*args, **kwargs):
    pass

n = 8000

printdead, printlive = '_#'
maxgenerations = n
cellcount = 5000
offendvalue = '0'
 
universe = ''.join(random.choice('01') for i in range(cellcount))
 
neighbours2newstate = {
 '000': '0',
 '001': '0',
 '010': '0',
 '011': '1',
 '100': '0',
 '101': '1',
 '110': '1',
 '111': '0',
 }
 
for i in range(maxgenerations):
    print("Generation %3i:  %s" % ( i,
          universe.replace('0', printdead).replace('1', printlive) ))
    universe = offendvalue + universe + offendvalue
    universe = ''.join(neighbours2newstate[universe[i:i+3]] for i in range(cellcount))

