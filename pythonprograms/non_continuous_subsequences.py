n = 22
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Non-continuous_subsequences#Python

def ncsub(seq, s=0):
    if seq:
        x = seq[:1]
        xs = seq[1:]
        p2 = s % 2
        p1 = not p2
        return [x + ys for ys in ncsub(xs, s + p1)] + ncsub(xs, s + p2)
    else:
        return [[]] if s >= 3 else []

n = {n}

ncsub(list(range(1, n)))


"""
