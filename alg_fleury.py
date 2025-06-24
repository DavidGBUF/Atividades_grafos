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
    vertices_fechados = []

    while True:
        # Verifica se todas as arestas foram removidas
        if np.array_equal(matriz_adj, np.zeros((tam, tam), dtype=int)):
            return resposta

        # Tenta remover uma aresta segura
        for i, value in enumerate(matriz_adj[index_node]):
            if value:
                # Se é a única aresta do vértice, deve ser usada
                if np.count_nonzero(matriz_adj[index_node]) == 1:
                    resposta, matriz_adj, current_node, index_node, vertices_fechados = \
                        processar_aresta_unica(resposta, matriz_adj, current_node, index_node, i, vertices_fechados, G)
                    break

                # Testa se a aresta é uma ponte
                aux = deepcopy(matriz_adj)
                aux[index_node][i] = 0
                aux[i][index_node] = 0
                if G.conexo_por_mm(m=aux, ignorar_indices=vertices_fechados):
                    resposta, matriz_adj, current_node, index_node = \
                        processar_aresta_segura(resposta, aux, current_node, index_node, i, G)
                    break
        else:
            # Se nenhuma aresta segura foi encontrada, pega qualquer uma
            resposta, matriz_adj, current_node, index_node = \
                processar_aresta_qualquer(resposta, matriz_adj, current_node, index_node, G)

    return resposta


def processar_aresta_unica(resposta, matriz_adj, current_node, index_node, i, vertices_fechados, G):
    vertices_fechados.append(index_node)
    matriz_adj[index_node][i] = 0
    matriz_adj[i][index_node] = 0
    resposta.append((current_node, G.vertices[i]))
    current_node = G.vertices[i]
    index_node = i
    return resposta, matriz_adj, current_node, index_node, vertices_fechados


def processar_aresta_segura(resposta, matriz_adj, current_node, index_node, i, G):
    matriz_adj[index_node][i] = 0
    matriz_adj[i][index_node] = 0
    resposta.append((current_node, G.vertices[i]))
    current_node = G.vertices[i]
    index_node = i
    return resposta, matriz_adj, current_node, index_node


def processar_aresta_qualquer(resposta, matriz_adj, current_node, index_node, G):
    for i, value in enumerate(matriz_adj[index_node]):
        if value:
            matriz_adj[index_node][i] = 0
            matriz_adj[i][index_node] = 0
            resposta.append((current_node, G.vertices[i]))
            current_node = G.vertices[i]
            index_node = i
            break
    else:
        return False, None, None, None
    return resposta, matriz_adj, current_node, index_node


# Teste do algoritmo de Fleury
g = Grafo(
    vertices=[1, 2, 3, 4, 5, 6, 7, 8, 9],
    direcionado=False,
    arestas=[
        (1, 2), (1, 5),
        (2, 3), (2, 5), (2, 4),
        (3, 6),
        (4, 5), (4, 8), (4, 7),
        (5, 6), (5, 9), (5, 8),
        (7, 8),
        (8, 9)
    ]
)
print(alg_fleury(g))
