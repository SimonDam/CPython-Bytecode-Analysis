def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Knuth_shuffle#Python

from random import randrange, seed
seed(89732465987234658972346587932465873264)

def knuth_shuffle(x):
    for i in range(len(x)-1, 0, -1):
        j = randrange(i + 1)
        x[i], x[j] = x[j], x[i]

def print(*args, **kwargs):
    pass

n = {n}
x = list(range(n))
knuth_shuffle(x)
print("shuffled:", x)

"""
