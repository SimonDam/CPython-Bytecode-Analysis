def source_code(n):	
    return f"""# Written by Simon Dam Nielsen

import random
random.seed(9384750293475980234750982347509832475987)

def bubble_sort(lst):
    for j in range(len(lst)):
        for i in range(1, len(lst)-j):
            if lst[i-1] > lst[i]:
                lst[i], lst[i-1] = lst[i-1], lst[i]
    return lst
n = {n}
bubble_sort([random.randint(1,10**10) for _ in range(n)])

"""
