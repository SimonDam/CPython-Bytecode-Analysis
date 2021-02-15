# Taken from: https://www.rosettacode.org/wiki/Cantor_set#Python

n = 5500

WIDTH = n
HEIGHT = n
 
lines=[]
def cantor(start, len, index):
    seg = len // 3
    if seg == 0:
        return None
    for it in range(HEIGHT-index):
        i = index + it
        for jt in range(seg):
            j = start + seg + jt
            pos = i * WIDTH + j
            lines[pos] = ' '
    cantor(start,           seg, index + 1)
    cantor(start + seg * 2, seg, index + 1)
    return None
 
lines = ['*'] * (WIDTH*HEIGHT)
cantor(0, WIDTH, 1)

def print(*args, **kwargs):
    pass

for i in range(HEIGHT):
    beg = WIDTH * i
    print(''.join(lines[beg : beg+WIDTH]))

