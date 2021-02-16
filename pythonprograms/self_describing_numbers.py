n = 6815743
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Self-describing_numbers#Python

def isSelfDescribing(n):
    s = str(n)
    return all(s.count(str(i)) == int(ch) for i, ch in enumerate(s))

def print(*args, **kwargs):
    pass

n = {n}

print([x for x in range(n) if isSelfDescribing(x)])


"""
