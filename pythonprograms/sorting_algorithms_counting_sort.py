n = 4194303
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Sorting_algorithms/Counting_sort#Python

from collections import defaultdict
def countingSort(array, mn, mx):
    count = defaultdict(int)
    for i in array:
        count[i] += 1
    result = []
    for j in range(mn,mx+1):
        result += [j]* count[j]
    return result

import random
random.seed(46753892658732498576234857)

n = {n}
data = [random.randint(1, n) for _ in range(n)]
mini,maxi = 1,n
countingSort(data, mini, maxi) == sorted(data)

"""
