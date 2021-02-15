# Taken from: https://www.rosettacode.org/wiki/Self-describing_numbers#Python

def isSelfDescribing(n):
    s = str(n)
    return all(s.count(str(i)) == int(ch) for i, ch in enumerate(s))

def print(*args, **kwargs):
    pass

n = 5000000

print([x for x in range(n) if isSelfDescribing(x)])


