n = 2359295
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Van_der_Corput_sequence#Python

def vdc(n, base=2):
    vdc, denom = 0,1
    while n:
        denom *= base
        n, remainder = divmod(n, base)
        vdc += remainder / denom
    return vdc

def print(*args, **kwargs):
    pass

n = {n}
print([vdc(i) for i in range(n)])



"""
