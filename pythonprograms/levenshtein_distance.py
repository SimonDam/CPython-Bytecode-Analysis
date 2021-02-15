# Taken from: https://www.rosettacode.org/wiki/Levenshtein_distance#Python

def minimumEditDistance(s1,s2):
    if len(s1) > len(s2):
        s1,s2 = s2,s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]

def print(*args, **kwargs):
    pass


print(minimumEditDistance("kitten","sitting"))
print(minimumEditDistance("rosettacode","raisethysword"))

import random
random.seed(982375498723)
import string

n = 4000
minimumEditDistance(''.join(random.choice(string.ascii_letters) for _ in range(n)), ''.join(random.choice(string.ascii_letters) for _ in range(n)))

