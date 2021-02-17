n = 16777215
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Van_Eck_sequence#Python

from itertools import islice

def van_eck():
    n, seen, val = 0, {{}}, 0
    while True:
        yield val
        last = {{val: n}}
        val = n - seen.get(val, n)
        seen.update(last)
        n += 1

def print(*args, **kwargs):
    pass

n = {n}
if __name__ == '__main__':
    print("Van Eck: first 10 terms:  ", list(islice(van_eck(), 10)))
    print("Van Eck: terms 991 - 1000:", list(islice(van_eck(), 1000))[-10:])
    print("Van Eck: terms 991 - 1000:", list(islice(van_eck(), n)))


"""
