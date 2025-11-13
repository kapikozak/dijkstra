from collections import namedtuple
edge = namedtuple('edge', 'weight, dst')

def instantiate_graph(filename):
    graph = {}

    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            line = line.strip()
            vert, a_list = line.split(':')
            pairs = [p.strip() for p in a_list.split(',') if p.strip()]
            edges = []
            for p in pairs:
                weight, dst = map(int, p.split())
                edges.append(edge(weight, dst))

            graph[int(vert)] = edges
            line = f.readline()
        return graph

prio_check = lambda vertices, h, i, j: vertices[h[i]]['d'] < vertices[h[j]]['d']

def up_heap(vertices, h, n):
    while n > 0:
        i = (n - 1) // 2
        if prio_check(vertices, h, n, i):
            h[n], h[i] = h[i], h[n]
            vertices[h[n]]['h_idx'], vertices[h[i]]['h_idx'] = n, i

            n = i
        else:
            break

def down_heap(vertices, h, f):
    n = len(h)
    i = 2*f+1
    while i < n:
        j = i+1
        if j < n and prio_check(vertices, h, j, i):
            i = j
        if prio_check(vertices, h, i, f):
            h[i], h[f] = h[f], h[i]
            vertices[h[i]]['h_idx'], vertices[h[f]]['h_idx'] = i, f

            f = i
            i = 2*f+1
        else:
            break

def remove_min(vertices, h):
    n = len(h)
    h[0], h[n-1] = h[n-1], h[0]
    vertices[h[0]]['h_idx'], vertices[h[n-1]]['h_idx'] = 0, -1
    v = h.pop()
    down_heap(vertices, h, 0)

    return v


def dijkstra(graph, u):
    def init_single_source(vert):
        v_dict = {
            vert : {
                'd': 0,
                'p': None,
                'h_idx': 0
            }
        }

        v_heap = [vert]

        for k in graph:
            if k != vert:
                v_dict[k] = {
                    'd': float('inf'),
                    'p': None,
                    'h_idx': len(v_heap)
                }
                v_heap.append(k)

        return v_dict, v_heap

    def drop_h_idx(v_dict):
        for k in v_dict:
            v_dict[k].pop('h_idx')

    vertices, h = init_single_source(u)
    while h:
        v = remove_min(vertices, h)
        for e in graph[v]:
            if vertices[e.dst]['d'] > vertices[v]['d'] + e.weight:
                vertices[e.dst]['d'] = vertices[v]['d'] + e.weight
                vertices[e.dst]['p'] = v
                up_heap(vertices, h, vertices[e.dst]['h_idx'])

    drop_h_idx(vertices)
    return vertices

if __name__ == '__main__':
    g = instantiate_graph('graph.txt')
    vs = dijkstra(g, 1)
    print(vs)