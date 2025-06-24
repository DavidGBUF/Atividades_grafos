from grafo_utils import Grafo
def dfs(G: Grafo, no_init = None):
    cor = {}
    pi = {}
    d = {}
    f = {}
    for v in G.vertices:
        cor[v] = 'BRANCO'
        pi[v] = None
    
    time = [0]
    vertices = G.vertices
    if no_init:
        idx_no_init = vertices.index(no_init)
        v0 = vertices[0]
        vertices[0] = no_init
        vertices[idx_no_init] = v0

    for v in vertices:
        if cor[v] == 'BRANCO':
            dfs_visit(G,v, cor, pi,time, d, f)

def dfs_visit(G: Grafo,v, cor, pi, time, d, f):
    cor[v] = 'CINZA'
    time[0]+=1
    d[v] = time[0]

    print(f"DFS({v})")
    print(f"Cor[{v}] = {cor[v]}")
    print(f"D[{v}] = {d[v]}")
    print(f"Pi[{v}] = {pi[v]}")
    print("\n===============================")

    adjs_ordenados = sorted(G.lista_adjacencias()[v])
    for v_adj in adjs_ordenados:
        if cor[v_adj] == 'BRANCO':
            pi[v_adj] = v
            dfs_visit(G, v_adj, cor, pi, time, d, f)

    cor[v] = 'PRETO'
    print(f"Cor[{v}] = {cor[v]}")
    f[v] = time[0] = time[0]+1
    print(f"F[{v}] = {f[v]}")

grafo = Grafo(vertices=[1,2,3,4,5,6,7], arestas=[(1,2),(1,3),(1,4),(2,4),(2,6),(6,5), (6,7) ,(5,7),(7,4), (4,3)], direcionado=False)

dfs(grafo, no_init=2)





            


