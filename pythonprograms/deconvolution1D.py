# Taken from: https://www.rosettacode.org/wiki/Deconvolution/1D#Python

def ToReducedRowEchelonForm( M ):
    if not M: return
    lead = 0
    rowCount = len(M)
    columnCount = len(M[0])
    for r in range(rowCount):
        if lead >= columnCount:
            return
        i = r
        while M[i][lead] == 0:
            i += 1
            if i == rowCount:
                i = r
                lead += 1
                if columnCount == lead:
                    return
        M[i],M[r] = M[r],M[i]
        lv = M[r][lead]
        M[r] = [ mrx / lv for mrx in M[r]]
        for i in range(rowCount):
            if i != r:
                lv = M[i][lead]
                M[i] = [ iv - lv*rv for rv,iv in zip(M[r],M[i])]
        lead += 1
    return M
 
def pmtx(mtx):
    print ('\n'.join(''.join(' %4s' % col for col in row) for row in mtx))
 
def convolve(f, h):
    g = [0] * (len(f) + len(h) - 1)
    for hindex, hval in enumerate(h):
        for findex, fval in enumerate(f):
            g[hindex + findex] += fval * hval
    return g
 
def deconvolve(g, f):
    lenh = len(g) - len(f) + 1
    mtx = [[0 for x in range(lenh+1)] for y in g]
    for hindex in range(lenh):
        for findex, fval in enumerate(f):
            gindex = hindex + findex
            mtx[gindex][hindex] = fval
    for gindex, gval in enumerate(g):        
        mtx[gindex][lenh] = gval
    ToReducedRowEchelonForm( mtx )
    return [mtx[i][lenh] for i in range(lenh)]  # h

def print(*args, **kwargs):
    pass
 
import random
random.seed(8973465982346589234875)

n = 425
if __name__ == '__main__':
    f = int(n/10)
    h = [random.randint(1,10) for _ in range(n)]
    f = [random.randint(1,10) for _ in range(f)]
    g = [random.randint(1,10) for _ in range(n)]
    print(len(h))
    print(len(f))
    print(len(g))
    convolve(f,h)
    deconvolve(g, f)

