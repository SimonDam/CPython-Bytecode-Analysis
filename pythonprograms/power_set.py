def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Power_set#Python

import random
random.seed(73465083974675038247560832475630248576)

def list_powerset(lst):
    # the power set of the empty set has one element, the empty set
    result = [[]]
    for x in lst:
        # for every additional element in our set
        # the power set consists of the subsets that don't
        # contain this element (just take the previous power set)
        # plus the subsets that do contain the element (use list
        # comprehension to add [x] onto everything in the
        # previous power set)
        result.extend([subset + [x] for subset in result])
    return result
 
# the above function in one statement
def list_powerset2(lst):
    return reduce(lambda result, x: result + [subset + [x] for subset in result],
                  lst, [[]])
 
def powerset(s):
    return frozenset(map(frozenset, list_powerset(list(s))))

n = {n}
list_powerset([random.randint(1, n) for _ in range(n)])
powerset(frozenset([random.randint(1, n) for _ in range(n)]))

"""
