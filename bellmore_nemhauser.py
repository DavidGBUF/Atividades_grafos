# Algoritmo Bellmore-Nemhauser
# Entrada: Grafo G = (V, E) com n vértices
# Saída: Um ciclo hamiltoniano (possivelmente) de custo mínimo

# 1. Escolher um vértice inicial vi qualquer
# 2. H ← {vi}   // H representa o caminho parcial
# 3. enquanto |H| < n faça
#     a. Encontrar o vértice vk ∉ H mais próximo de vi
#     b. H ← H ∪ {vk}
#     c. i ← k
# 4. fim enquanto
# 5. Retornar H como ciclo hamiltoniano aproximado

from grafo_utils import Grafo

def bellmore_nemhauser(G: Grafo):
    vertices = G.vertices
    arestas = G.arestas
    v=vertices[0]
    H = [v]
    while len(H) < len(vertices):
        menor_c = float("inf")
        menor_v = None
        for a in arestas:
            mesmo_v = a[0] == v
            custo_menor = arestas[a] < menor_c
            v_livre = a[1] not in H
            if  mesmo_v and  custo_menor and v_livre:
                menor_c = arestas[a]
                menor_v = a[1]
        if v == menor_v:
            return False
        else:
            v = menor_v
            H.append(v)
    if (H[0],H[-1]) not in arestas:
        return False
    H.append(H[0])
    return H

g = Grafo(vertices=['a','b','c','d'], direcionado=False, arestas={('a','b'):3, ('a','c'):2, ('a','d'):7,
                                                                  ('b','c'):5,('b','d'):9, ('c','d'):6})
print(bellmore_nemhauser(g))
        