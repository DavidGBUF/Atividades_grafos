from grafo_utils import Grafo
def dfs(G: Grafo):
    cor = {}
    pi = {}
    d = {}
    f = {}
    for v in G.vertices:
        cor[v] = 'BRANCO'
        pi[v] = None
    
    time = 0
    for v in G.vertices:
        if cor[v] == 'BRANCO':
            dfs_visit(G,v, cor, pi,time, d, f)

def dfs_visit(G: Grafo,v, cor, pi, time, d, f):
    cor[v] = 'CINZA'
    time+=1
    d[v] = time

    print(f"DFS({v})")
    print(f"Cor[{v}] = {cor[v]}")
    print(f"D[{v}] = {d[v]}")
    print(f"Pi[{v}] = {pi[v]}")
    print("\n===============================")

    for v_adj in G.lista_adjacencias[v].sort():
        if cor[v_adj] == 'BRANCO':
            pi[v_adj] = v
            dfs_visit(G, v_adj, cor, pi, time, d, f)

    cor[v] = 'PRETO'
    print(f"Cor[{v}] = {cor[v]}")
    f[v] = time = time+1
    print(f"F[{v}] = {f[v]}")

grafo = Grafo()





            


