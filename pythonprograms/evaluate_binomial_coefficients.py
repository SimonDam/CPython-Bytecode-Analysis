# Taken from: https://www.rosettacode.org/wiki/Evaluate_binomial_coefficients#Python

def binomialCoeff(n, k):
    result = 1
    for i in range(1, k+1):
        result = result * (n-i+1) / i
    return result

def print(*args, **kwargs):
    pass

n = 40000000
if __name__ == "__main__":
    print(binomialCoeff(0.0001, n))

