n = 20
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Fast_Fourier_transform#Python

from cmath import exp, pi
import random
random.seed(873645983469872)

def print(*args, **kwargs):
    pass

def fft(x):
    N = len(x)
    if N <= 1: return x
    even = fft(x[0::2])
    odd =  fft(x[1::2])
    T= [exp(-2j*pi*k/N)*odd[k] for k in range(N//2)]
    return [even[k] + T[k] for k in range(N//2)] + \\
           [even[k] - T[k] for k in range(N//2)]
n = {n}
print( ' '.join("%5.3f" % abs(f) 
                for f in fft([random.randint(0,1) for _ in range(2**n)])) )

"""
