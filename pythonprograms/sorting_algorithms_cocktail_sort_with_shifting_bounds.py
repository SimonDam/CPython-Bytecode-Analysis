def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Sorting_algorithms/Cocktail_sort_with_shifting_bounds#Python

'''
 
Python example of
 
http://rosettacode.org/wiki/Sorting_algorithms/Cocktail_sort_with_shifting_bounds
 
based on 
 
http://rosettacode.org/wiki/Sorting_algorithms/Cocktail_sort#Python
 
'''
 
def cocktailshiftingbounds(A):
    beginIdx = 0
    endIdx = len(A) - 1
 
    while beginIdx <= endIdx:
        newBeginIdx = endIdx
        newEndIdx = beginIdx
        for ii in range(beginIdx,endIdx):
            if A[ii] > A[ii + 1]:
                A[ii+1], A[ii] = A[ii], A[ii+1]
                newEndIdx = ii
 
        endIdx = newEndIdx
 
        for ii in range(endIdx,beginIdx-1,-1):
            if A[ii] > A[ii + 1]:
                A[ii+1], A[ii] = A[ii], A[ii+1]
                newBeginIdx = ii
 
        beginIdx = newBeginIdx + 1

import random
random.seed(6926928735872369856)

def print(*args, **kwargs):
    pass

n = {n}
test1 = [random.randint(1, n) for _ in range(n)]
cocktailshiftingbounds(test1)
print(test1)
 
test2=list('big fjords vex quick waltz nymph')
cocktailshiftingbounds(test2)
print(''.join(test2))
 

"""
