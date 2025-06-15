from grafo_utils import Grafo
from copy import deepcopy
import numpy as np
def alg_fleury(G: Grafo):


    resposta = []
    tam = len(G.vertices)

    if not G.conexo_por_mm():
        raise Exception("Grafo não é conexo")

    matriz_adj = G.matriz_de_adjacencias()
    current_node = G.vertices[0]
    index_node = 0
    vertices_fechados=[]
    while True:
        if np.array_equal(matriz_adj, np.zeros((tam, tam), dtype=int)):
            return resposta

        for i, value in enumerate(matriz_adj[index_node]):
            if value:
                # Se é a única aresta do vértice, deve ser usada
                if np.count_nonzero(matriz_adj[index_node]) == 1:
                    vertices_fechados.append(index_node)
                    matriz_adj[index_node][i] = 0
                    matriz_adj[i][index_node] = 0
                    resposta.append((current_node, G.vertices[i]))
                    current_node = G.vertices[i]
                    index_node = i

                    break

                # Testa se é ponte
                aux = deepcopy(matriz_adj)
                aux[index_node][i] = 0
                aux[i][index_node] = 0
                if G.conexo_por_mm(m=aux, ignorar_indices=vertices_fechados):
                    matriz_adj = aux
                    resposta.append((current_node, G.vertices[i]))
                    current_node = G.vertices[i]
                    index_node = i
                    break
        else:
            # Se nenhuma aresta segura foi encontrada, pegue qualquer uma
            for i, value in enumerate(matriz_adj[index_node]):
                if value:
                    matriz_adj[index_node][i] = 0
                    matriz_adj[i][index_node] = 0
                    resposta.append((current_node, G.vertices[i]))
                    current_node = G.vertices[i]
                    index_node = i
                    break
            else:
                return False

        

g = Grafo(
    vertices=[1,2,3,4,5,6],
    direcionado=False,
    arestas=[
        (1,2), (1,3),(1,5),
        (2,4), (2,6),
        (3,6),(3,4),
        (4,5),
        (5,6),
    ]
)
print(alg_fleury(g))
                    
    