def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Munchausen_numbers#Python

def print(*args, **kwargs):
    pass

n = {n}
for i in range(n):
    if i == sum(int(x) ** int(x) for x in str(i)):
        print(i)

"""
