n = 7679
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Matrix-exponentiation_operator#Python

class Mat(list) :
    def __matmul__(self, B) :
        A = self
        return Mat([[sum(A[i][k]*B[k][j] for k in range(len(B)))
                    for j in range(len(B[0])) ] for i in range(len(A))])
 
def identity(size):
    size = range(size)
    return [[(i==j)*1 for i in size] for j in size]
 
def power(F, n):
    result = Mat(identity(len(F)))
    b = Mat(F)
    while n > 0:
        if (n%2) == 0:
            b = b @ b
            n //= 2
        else:
            result = b @ result
            b = b @ b
            n //= 2
    return result
 
def printtable(data):
    for row in data:
        print (' '.join('%-5s' % ('%s' % cell) for cell in row))

def print(*args, **kwargs):
    pass

n = {n}

m = [[3,2], [2,1]]
for i in range(n):
    print('\\n%i:' % i)
    printtable(power(m, i))

"""
