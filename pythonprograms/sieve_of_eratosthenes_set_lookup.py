n = 23068671
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Sieve_of_Eratosthenes#Python

def eratosthenes2(n):
    multiples = set()
    for i in range(2, n+1):
        if i not in multiples:
            yield i
            multiples.update(range(i*i, n+1, i))

def print(*args, **kwargs):
    pass

n = {n}
print(list(eratosthenes2(n)))

"""
