def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Department_numbers#Python

def print(*args, **kwargs):
    pass

from itertools import permutations

def solve(n):
    c, p, f, s = "\\\\,Police,Fire,Sanitation".split(',')
    print(f"{{c:>3}}  {{p:^6}} {{f:^4}} {{s:^10}}")
    c = 1
    for p, f, s in permutations(range(1, n), r=3):
        if p + s + f == 12 and p % 2 == 0:
            print(f"{{c:>3}}: {{p:^6}} {{f:^4}} {{s:^10}}")
            c += 1
 
n = {n}
if __name__ == '__main__':
    solve(n)

"""
