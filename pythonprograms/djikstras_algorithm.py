def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Dijkstra%27s_algorithm#Python

from collections import namedtuple, deque
from pprint import pprint as pp
import random
random.seed(8732649813687963249875623489758932465)
import string
 
inf = float('inf')
Edge = namedtuple('Edge', ['start', 'end', 'cost'])
 
class Graph():
    def __init__(self, edges):
        self.edges = [Edge(*edge) for edge in edges]
        # print(dir(self.edges[0]))
        self.vertices = {{e.start for e in self.edges}} | {{e.end for e in self.edges}}
 
    def dijkstra(self, source, dest):
        assert source in self.vertices
        dist = {{vertex: inf for vertex in self.vertices}}
        previous = {{vertex: None for vertex in self.vertices}}
        dist[source] = 0
        q = self.vertices.copy()
        neighbours = {{vertex: set() for vertex in self.vertices}}
        for start, end, cost in self.edges:
            neighbours[start].add((end, cost))
        #pp(neighbours)
 
        while q:
            # pp(q)
            u = min(q, key=lambda vertex: dist[vertex])
            q.remove(u)
            if dist[u] == inf or u == dest:
                break
            for v, cost in neighbours[u]:
                alt = dist[u] + cost
                if alt < dist[v]:                                  # Relax (u,v,a)
                    dist[v] = alt
                    previous[v] = u
        #pp(previous)
        s, u = deque(), dest
        while previous[u]:
            s.appendleft(u)
            u = previous[u]
        s.appendleft(u)
        return s

n = {n}
g_list_1 = [random.choice(string.ascii_letters) for _ in range(n)]
g_list_2 = g_list_1.copy()
random.shuffle(g_list_2)
l_list = [random.randint(1,n) for _ in range(n)]
g_list = [(a, b, c) for a, b, c in zip(g_list_1, g_list_2, l_list)]
graph = Graph(g_list)

def pp(*args, **kwargs):
    pass

#
#for _ in range(n):
#    pp(graph.dijkstra(random.choice(g_list)[0], random.choice(g_list)[1]))
#

"""
