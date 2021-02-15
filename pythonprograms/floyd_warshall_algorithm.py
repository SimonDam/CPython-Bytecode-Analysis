def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Floyd-Warshall_algorithm#Python

from math import inf
from itertools import product
 
def floyd_warshall(n, edge):
    rn = range(n)
    dist = [[inf] * n for i in rn]
    nxt  = [[0]   * n for i in rn]
    for i in rn:
        dist[i][i] = 0
    for u, v, w in edge:
        dist[u-1][v-1] = w
        nxt[u-1][v-1] = v-1
    for k, i, j in product(rn, repeat=3):
        sum_ik_kj = dist[i][k] + dist[k][j]
        if dist[i][j] > sum_ik_kj:
            dist[i][j] = sum_ik_kj
            nxt[i][j]  = nxt[i][k]
    print("pair     dist    path")
    for i, j in product(rn, repeat=2):
        if i != j:
            path = [i]
            while path[-1] != j:
                path.append(nxt[path[-1]][j])
            print("%d → %d  %4d       %s" 
                  % (i + 1, j + 1, dist[i][j], 
                     ' → '.join(str(p + 1) for p in path)))

def print(*args, **kwargs):
    pass

n = {n}
if __name__ == '__main__':
    lst = [[a, b, c] for a, b, c in zip(list(range(0,n)), list(range(1,n+1)), list(range(2,n+2)))]
    floyd_warshall(n, lst)

"""
