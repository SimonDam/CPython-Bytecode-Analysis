n = 1179647
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Factorions#Python

def print(*args, **kwargs):
    pass

fact = [1] # cache factorials from 0 to 11
for t in range(1, 12):
    fact.append(fact[t-1] * t)
 

n = {n}

for b in range(9, 12+1):
    print(f"The factorions for base {{b}} are:")
    for i in range(n):
        fact_sum = 0
        j = i
        while j > 0:
            d = j % b
            fact_sum += fact[d]
            j = j//b
        if fact_sum == i:
            print(i, end=" ")
    print()

"""
