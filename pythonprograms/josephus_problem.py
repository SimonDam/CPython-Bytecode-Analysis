def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Josephus_problem#Python

def j(n, k):
    p, i, seq = list(range(n)), 0, []
    while p:
        i = (i+k-1) % len(p)
        seq.append(p.pop(i))
    return 'Prisoner killing order: %s.\\nSurvivor: %i' % (', '.join(str(i) for i in seq[:-1]), seq[-1])

def print(*args, **kwargs):
    pass

n = {n}
print(j(n, 10))

"""
