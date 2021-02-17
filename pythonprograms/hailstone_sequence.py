n = 425984
min_n = 2
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Hailstone_sequence#Python

def hailstone(n):
    seq = [n]
    while n>1:
        n = 3*n + 1 if n & 1 else n//2
        seq.append(n)
    return seq
 
def print(*args, **kwargs):
    pass

n = {n}
if __name__ == '__main__':
    h = hailstone(27)
    assert len(h)==112 and h[:4]==[27, 82, 41, 124] and h[-4:]==[8, 4, 2, 1]

    print("Maximum length %i was found for hailstone(%i) for numbers <100,000" %
          max((len(hailstone(i)), i) for i in range(1,n)))

"""
