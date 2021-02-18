def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Pythagorean_quadruples#Python

def quad(top=2200):
    r = [False] * top
    ab = [False] * (top * 2)**2
    for a in range(1, top):
        for b in range(a, top):
            ab[a * a + b * b] = True
    s = 3
    for c in range(1, top):
        s1, s, s2 = s, s + 2, s + 2
        for d in range(c + 1, top):
            if ab[s1]:
                r[d] = True
            s1 += s2
            s2 += 2
    return [i for i, val in enumerate(r) if not val and i]

def print(*args, **kwargs):
    pass

n = {n}
if __name__ == '__main__':
    print(f"Those values of d in 1..{{n}} that can't be represented: {{quad(n)}}")

"""
