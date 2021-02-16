n = 15615
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Longest_common_substring#Python

import random
random.seed(68457292874)

def print(*args, **kwargs):
    pass

n = {n}
letters = "qwertyuiopasdfghjklzxcvbnm"
s1 = ''.join(random.choice(letters) for _ in range(n))
s2 = ''.join(random.choice(letters) for _ in range(n))
len1, len2 = len(s1), len(s2)
ir, jr = 0, -1
for i1 in range(len1):
    i2 = s2.find(s1[i1])
    while i2 >= 0:
        j1, j2 = i1, i2
        while j1 < len1 and j2 < len2 and s2[j2] == s1[j1]:
            if j1-i1 >= jr-ir:
                ir, jr = i1, j1
            j1 += 1; j2 += 1
        i2 = s2.find(s1[i1], i2+1)
print (s1[ir:jr+1])

"""
