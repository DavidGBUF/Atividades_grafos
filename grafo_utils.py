import numpy as np

class Grafo:
    def __init__(self, vertices: list, arestas, direcionado=True):
        self.direcionado = direcionado
        self.vertices = self._validar_vertices(vertices)
        self.arestas = self._validar_arestas(arestas)

    def _validar_vertices(self, vertices):
        for v in vertices:
            if not isinstance(v, (str, int)):
                raise ValueError("Os labels dos vértices devem ser inteiros ou strings")
        return vertices

    def _validar_arestas(self, arestas):
        if isinstance(arestas, list):
            return self._validar_arestas_lista(arestas)
        elif isinstance(arestas, dict):
            return self._validar_arestas_dicionario(arestas)
        else:
            raise ValueError("Arestas devem ser listas ou dicionários")

    def _validar_arestas_lista(self, arestas):
        valid_arestas = []
        for aresta in arestas:
            if not isinstance(aresta, tuple) or len(aresta) != 2:
                raise ValueError("Arestas devem ser tuplas e ter tamanho 2")
            u, v = aresta
            if u not in self.vertices or v not in self.vertices:
                raise ValueError(f"Aresta {aresta} contém vértices não existentes")
            if not self.direcionado:
                valid_arestas.extend([(u, v), (v, u)])
            else:
                valid_arestas.append((u, v))
        return valid_arestas

    def _validar_arestas_dicionario(self, arestas):
        valid_arestas = {}
        for aresta, valor in arestas.items():
            if not isinstance(aresta, tuple) or len(aresta) != 2:
                raise ValueError("Arestas devem ser tuplas e ter tamanho 2")
            u, v = aresta
            if u not in self.vertices or v not in self.vertices:
                raise ValueError(f"Aresta {aresta} contém vértices não existentes")
            if not isinstance(valor, (int, float)):
                raise ValueError("Pesos das arestas devem ser numéricos")
            if not self.direcionado:
                valid_arestas[aresta] = valor
                valid_arestas[aresta[::-1]] = valor
            else:
                valid_arestas[aresta] = valor
        return valid_arestas

    def printar_grafo(self):
        print(f"G = (V = [{', '.join(map(str, self.vertices))}], A = [", end="")
        if isinstance(self.arestas, list):
            for i, a in enumerate(self.arestas):
                print(f"{a}", end="")
                if i != len(self.arestas) - 1:
                    print(", ", end="")
        else:
            for i, (a, peso) in enumerate(self.arestas.items()):
                print(f"{a}: {peso}", end="")
                if i != len(self.arestas) - 1:
                    print(", ", end="")
        print("])")

    def grau_entrada_dos_vertices(self):
        graus = {v: 0 for v in self.vertices}
        for aresta in self.arestas:
            if aresta[1] in graus:
                graus[aresta[1]] += 1
        return graus

    def grau_saida_dos_vertices(self):
        graus = {v: 0 for v in self.vertices}
        for aresta in self.arestas:
            if aresta[0] in graus:
                graus[aresta[0]] += 1
        return graus

    def graus_de_um_vertice(self, v):
        entrada = sum(1 for aresta in self.arestas if aresta[1] == v)
        saida = sum(1 for aresta in self.arestas if aresta[0] == v)
        return entrada, saida

    def verificar_aresta(self, aresta):
        return aresta in self.arestas

    def vertice_isolado(self, v):
        return all(v not in aresta for aresta in self.arestas)

    def adicionar_vertice(self, v):
        if not isinstance(v, (str, int, float)):
            raise ValueError("Vértice a adicionar deve ser string ou numérico")
        self.vertices.append(v)

    def adicionar_aresta(self, aresta):
        if not isinstance(aresta, tuple) or len(aresta) != 2:
            raise ValueError("Aresta deve ser tupla com tamanho 2")
        u, v = aresta
        if u not in self.vertices or v not in self.vertices:
            raise ValueError("Vértices não existem")
        if isinstance(self.arestas, list):
            self.arestas.append(aresta)
        else:
            self.arestas[aresta] = 0

    def lista_adjacencias(self):
        lista_adjacencias = {v: [] for v in self.vertices}
        for v1, v2 in self.arestas:
            if v1 in lista_adjacencias:
                lista_adjacencias[v1].append(v2)
        return lista_adjacencias

    def matriz_de_adjacencias(self):
        tam = len(self.vertices)
        matriz = [[0] * tam for _ in range(tam)]
        for i1, v1 in enumerate(self.vertices):
            for i2, v2 in enumerate(self.vertices):
                if (v1, v2) in self.arestas:
                    matriz[i1][i2] = 1
        return matriz

    def conexo_por_mm(self, m=None, ignorar_indices=None):
        tam = len(self.vertices)
        R = np.zeros((tam, tam), dtype=int)
        
        if m is None:
            m = self.matriz_de_adjacencias()

        if ignorar_indices is None:
            ignorar_indices = []

        for i in range(1, tam + 1):
            R += np.linalg.matrix_power(m, i)

        np.fill_diagonal(R, 1)

        # Marca como "conectado" os vértices ignorados entre si (e com os outros)
        for i in ignorar_indices:
            for j in range(tam):
                R[i][j] = 1
                R[j][i] = 1

        return np.all(R > 0)

if __name__ == "__main__":
    # Teste 1 – Grafo direcionado sem pesos
    print("Teste 1: Grafo direcionado simples")
    grafo1 = Grafo(vertices=[1, 2, 3], arestas=[(1, 2), (2, 3)])
    grafo1.printar_grafo()
    print("Grau de entrada:", grafo1.grau_entrada_dos_vertices())
    print("Grau de saída:", grafo1.grau_saida_dos_vertices())
    print("Graus do vértice 2:", grafo1.graus_de_um_vertice(2))
    print("Lista de adjacência:", grafo1.lista_adjacencias())
    print("Matriz de adjacência:")
    for linha in grafo1.matriz_de_adjacencias():
        print(linha)
    print("Vértice 3 é isolado?", grafo1.vertice_isolado(3))
    print()

    # Teste 2 – Adição de vértice e aresta
    print("Teste 2: Adicionando vértice e aresta")
    grafo1.adicionar_vertice(4)
    grafo1.adicionar_aresta((3, 4))
    grafo1.printar_grafo()
    print("Lista de adjacência atualizada:", grafo1.lista_adjacencias())
    print()

    # Teste 3 – Grafo com pesos
    print("Teste 3: Grafo com pesos")
    grafo2 = Grafo(vertices=['A', 'B'], arestas={('A', 'B'): 5})
    grafo2.printar_grafo()
    print("Verificar aresta ('A', 'B'):", grafo2.verificar_aresta(('A', 'B')))
    print("Matriz de adjacência:")
    for linha in grafo2.matriz_de_adjacencias():
        print(linha)
    print()
