from grafo_utils import Grafo

def bfs(G: Grafo, no_fonte):
    vertices = G.vertices[:]
    vertices.remove(no_fonte)
    cor={}
    pi={}
    d={}
    
    for u in vertices:
        d[u] = float('inf')
        cor[u]="BRANCO"
        pi[u] = None

    cor[no_fonte] = "CINZA"
    d[no_fonte] = 0
    pi[no_fonte] = None
    Q = []
    Q.append(no_fonte)
    print(f"BFS({no_fonte})")
    print(f"Cor[{no_fonte}] = {cor[no_fonte]}")
    print(f"D[{no_fonte}] = {d[no_fonte]}")
    print(f"PI[{no_fonte}] = {pi[no_fonte]}")
    print("\n=============================")
    while Q:
        u = Q.pop(0)
        lista_adj=G.lista_adjacencias()
        adj = sorted(lista_adj[u])
        print("==================")
        for v in adj:
            if cor[v] == "BRANCO":
                cor[v] = "CINZA"
                d[v] = d[u] + 1
                pi[v] = u
                print(f"BFS({v})")
                print(f"Cor[{v}] = {cor[v]}")
                print(f"D[{v}] = {d[v]}")
                print(f"PI[{v}] = {pi[v]}")
                print()
                Q.append(v)

        cor[u] = "PRETO"
        print(f"Cor[{u}] = {cor[u]}")






grafo = Grafo(vertices=[1,2,3,4,5,6,7,8], arestas=[(1,2),(1,8),(1,7),(1,6),(2,8),(8,7), (6,7) ,(6,3),(3,4), (4,5)], direcionado=False)
bfs(grafo, 7)







            


