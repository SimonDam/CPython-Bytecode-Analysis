# Taken from: https://www.rosettacode.org/wiki/Gray_code#Python

def gray_encode(n):
    return n ^ n >> 1
 
def gray_decode(n):
    m = n >> 1
    while m:
        n ^= m
        m >>= 1
    return n

def print(*args, **kwargs):
    pass
 
n = 1000000
if __name__ == '__main__':
    print("DEC,   BIN =>  GRAY => DEC")
    for i in range(n):
        gray = gray_encode(i)
        dec = gray_decode(gray)
        print(f" {i:>2d}, {i:>05b} => {gray:>05b} => {dec:>2d}")

