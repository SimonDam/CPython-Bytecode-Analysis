def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Evolutionary_algorithm#Python

from random import choice, random, seed
seed(13465865448683659745658387978578749)

def print(*args, **kwargs):
    pass

n = {n}
alphabet = " ABCDEFGHIJLKLMNOPQRSTUVWXYZ"
target  = list(''.join(choice(alphabet) for _ in range(n)))

p = 0.05 # mutation probability
c = 100  # number of children in each generation
 
def neg_fitness(trial):
    return sum(t != h for t,h in zip(trial, target))
 
def mutate(parent):
    return [(choice(alphabet) if random() < p else ch) for ch in parent]
 
parent = [choice(alphabet) for _ in range(len(target))]
i = 0
print("%3d" % i, "".join(parent))
while parent != target:
    copies = (mutate(parent) for _ in range(c))
    parent = min(copies, key=neg_fitness)
    print("%3d" % i, "".join(parent))
    i += 1

"""
