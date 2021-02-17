n = 33554431
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Jensen%27s_Device#Python

class Ref(object):
    def __init__(self, value=None):
        self.value = value
 
def harmonic_sum(i, lo, hi, term):
    # term is passed by-name, and so is i
    temp = 0
    i.value = lo
    while i.value <= hi:  # Python "for" loop creates a distinct which
        temp += term() # would not be shared with the passed "i"
        i.value += 1   # Here the actual passed "i" is incremented.
    return temp
 
i = Ref()
 
# note the correspondence between the mathematical notation and the
# call to sum it's almost as good as sum(1/i for i in range(1,101))

def print(*args, **kwargs):
    pass

n = {n}
print(harmonic_sum(i, 1, n, lambda: 1.0/i.value))

"""
