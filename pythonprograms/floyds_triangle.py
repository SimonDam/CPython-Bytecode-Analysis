# Taken from: https://www.rosettacode.org/wiki/Floyd%27s_triangle#Python

def floyd(rowcount=5):
    rows = [[1]]
    while len(rows) < rowcount:
        n = rows[-1][-1] + 1
        rows.append(list(range(n, n + len(rows[-1]) + 1)))
    return rows

n = 10000
floyd(n)

