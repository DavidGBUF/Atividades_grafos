from grafo_utils import Grafo

def floyd_warshall(grafo: Grafo):
    A = {}
    pi = {}
    arestas =  grafo.arestas
    for v in grafo.vertices:
        for w in grafo.vertices:
            if v == w:
                A[(v,w)] = 0
            else:
                if (v,w) not in arestas:
                    A[(v,w)] = float('inf')
                else: 
                    A[(v,w)] = arestas[(v,w)]

    for k in grafo.vertices:
        for v in grafo.vertices:
            for w in grafo.vertices:
                if A[v,k] + A[k,w] < A[v,w]:
                    A[v,w] = A[v,k] + A[k,w]
                    pi[w] = k

    return A, pi


if __name__ == "__main__":
    # Supondo que a classe 'Grafo' já esteja definida em seu ambiente

    print("Criação do Grafo da Imagem")
    grafo_imagem = Grafo(vertices=['1', '2', '3'],
                        arestas={('1', '1'): 2, 
                                ('1', '2'): 8, 
                                ('2', '1'): 3,
                                ('1', '3'): 5,
                                ('3', '2'): 2},
                        direcionado=True, 
                        ponderado=True)

    # Exibindo informações do grafo criado para verificação
    print("Arestas do grafo criado: ", grafo_imagem.arestas)
    grafo_imagem.printar_grafo()
    print("\nLista de adjacência (ponderada):", grafo_imagem.lista_adjacencias(ponderada=True))
    # print("\nMatriz de adjacência (ponderada):")
    # for linha in grafo_imagem.matriz_de_adjacencias(ponderada=True, default=0):
    #     print(linha)

    A, pi = floyd_warshall(grafo=grafo_imagem)

    print(A)

