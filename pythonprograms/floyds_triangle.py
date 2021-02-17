n = 18943
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Floyd%27s_triangle#Python

def floyd(rowcount=5):
    rows = [[1]]
    while len(rows) < rowcount:
        n = rows[-1][-1] + 1
        rows.append(list(range(n, n + len(rows[-1]) + 1)))
    return rows

n = {n}
floyd(n)

"""
