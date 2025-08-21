import numpy as np

class Grafo:
    def __init__(self, vertices: list, arestas, direcionado=True, ponderado=False):
        """
        vertices: lista de labels (str/int)
        arestas:
            - se ponderado=False: lista de tuplas (u, v)
            - se ponderado=True:
                * dict { (u, v): peso }  OU
                * lista de tuplas (u, v, peso)
        direcionado: True/False
        ponderado: True/False
        """
        self.direcionado = direcionado
        self.ponderado = ponderado
        self.vertices = self._validar_vertices(vertices)
        self._validar_entrada_arestas(arestas)

    # -------------------- validações internas --------------------
    def _validar_vertices(self, vertices):
        for v in vertices:
            if not isinstance(v, (str, int)):
                raise ValueError("Os labels dos vértices devem ser inteiros ou strings")
        return list(vertices)

    def _validar_entrada_arestas(self, arestas):
        """
        Normaliza o armazenamento:
          - se ponderado=False: self.arestas é uma LISTA de (u, v)
          - se ponderado=True : self.arestas é um DICIONÁRIO {(u, v): peso}
        """
        if not self.ponderado:
            # não ponderado: aceita apenas lista de (u, v)
            if not isinstance(arestas, list):
                raise ValueError("Para grafo não ponderado, arestas deve ser uma lista de (u, v)")
            self.arestas = self._validar_arestas_lista_nao_ponderada(arestas)
        else:
            # ponderado: aceita dict {(u, v): peso} ou lista [(u, v, w)]
            if isinstance(arestas, dict):
                self.arestas = self._validar_arestas_dicionario_ponderado(arestas)
            elif isinstance(arestas, list):
                self.arestas = self._validar_arestas_lista_ponderada(arestas)
            else:
                raise ValueError("Para grafo ponderado, forneça dict {(u,v): peso} ou lista [(u,v,peso)]")

    def _validar_arestas_lista_nao_ponderada(self, arestas):
        valid_arestas = []
        for aresta in arestas:
            if not isinstance(aresta, tuple) or len(aresta) != 2:
                raise ValueError("Arestas devem ser tuplas (u, v) para grafo não ponderado")
            u, v = aresta
            if u not in self.vertices or v not in self.vertices:
                raise ValueError(f"Aresta {aresta} contém vértices não existentes")
            if not self.direcionado:
                valid_arestas.extend([(u, v), (v, u)])
            else:
                valid_arestas.append((u, v))
        return valid_arestas

    def _validar_arestas_lista_ponderada(self, arestas):
        """
        Converte lista [(u,v,w)] em dict {(u,v): w}, duplicando se não-direcionado.
        """
        valid_arestas = {}
        for aresta in arestas:
            if (not isinstance(aresta, tuple)) or len(aresta) != 3:
                raise ValueError("Em grafo ponderado, use tuplas (u, v, peso)")
            u, v, w = aresta
            if u not in self.vertices or v not in self.vertices:
                raise ValueError(f"Aresta {aresta} contém vértices não existentes")
            if not isinstance(w, (int, float)):
                raise ValueError("Pesos das arestas devem ser numéricos")
            valid_arestas[(u, v)] = w
            if not self.direcionado:
                valid_arestas[(v, u)] = w
        return valid_arestas

    def _validar_arestas_dicionario_ponderado(self, arestas):
        valid_arestas = {}
        for aresta, valor in arestas.items():
            if not isinstance(aresta, tuple) or len(aresta) != 2:
                raise ValueError("Chaves do dicionário devem ser tuplas (u, v)")
            u, v = aresta
            if u not in self.vertices or v not in self.vertices:
                raise ValueError(f"Aresta {aresta} contém vértices não existentes")
            if not isinstance(valor, (int, float)):
                raise ValueError("Pesos das arestas devem ser numéricos")
            valid_arestas[(u, v)] = valor
            if not self.direcionado:
                valid_arestas[(v, u)] = valor
        return valid_arestas

    # -------------------- impressão --------------------
    def printar_grafo(self):
        print(f"G = (V = [{', '.join(map(str, self.vertices))}], A = [", end="")
        if not self.ponderado:
            for i, a in enumerate(self.arestas):
                print(f"{a}", end="")
                if i != len(self.arestas) - 1:
                    print(", ", end="")
        else:
            itens = list(self.arestas.items())
            for i, (a, peso) in enumerate(itens):
                print(f"{a}: {peso}", end="")
                if i != len(itens) - 1:
                    print(", ", end="")
        print("])")

    # -------------------- utilitários internos --------------------
    def _iter_arcos(self):
        """
        Itera sobre arestas como (u, v) (independente de ponderação).
        """
        if not self.ponderado:
            for (u, v) in self.arestas:
                yield (u, v)
        else:
            for (u, v) in self.arestas.keys():
                yield (u, v)

    def _iter_arcos_pesos(self):
        """
        Itera sobre arestas como (u, v, w).
        Para não ponderado, retorna w = 1 por convenção.
        """
        if not self.ponderado:
            for (u, v) in self.arestas:
                yield (u, v, 1)
        else:
            for (u, v), w in self.arestas.items():
                yield (u, v, w)

    # -------------------- graus --------------------
    def grau_entrada_dos_vertices(self):
        graus = {v: 0 for v in self.vertices}
        for (u, v) in self._iter_arcos():
            if v in graus:
                graus[v] += 1
        return graus

    def grau_saida_dos_vertices(self):
        graus = {v: 0 for v in self.vertices}
        for (u, v) in self._iter_arcos():
            if u in graus:
                graus[u] += 1
        return graus

    def graus_de_um_vertice(self, v):
        entrada = sum(1 for (u, w) in self._iter_arcos() if w == v)
        saida   = sum(1 for (u, w) in self._iter_arcos() if u == v)
        return entrada, saida

    # -------------------- consultas --------------------
    def verificar_aresta(self, aresta):
        """
        Aceita:
          - (u, v)   -> checa existência da aresta
          - (u, v, w) se ponderado=True -> checa existência com aquele peso exato
        """
        if not isinstance(aresta, tuple):
            return False

        if not self.ponderado:
            if len(aresta) != 2:
                return False
            return (aresta in self.arestas)
        else:
            if len(aresta) == 2:
                return (aresta in self.arestas)  # checa chave (u, v)
            elif len(aresta) == 3:
                u, v, w = aresta
                return self.arestas.get((u, v), None) == w
            else:
                return False

    def vertice_isolado(self, v):
        for (u, w) in self._iter_arcos():
            if v == u or v == w:
                return False
        return True

    # -------------------- modificações --------------------
    def adicionar_vertice(self, v):
        if not isinstance(v, (str, int, float)):
            raise ValueError("Vértice a adicionar deve ser string ou numérico")
        if v in self.vertices:
            return
        self.vertices.append(v)

    def adicionar_aresta(self, u, v, peso=None):
        if u not in self.vertices or v not in self.vertices:
            raise ValueError("Vértices não existem")

        if not self.ponderado:
            if peso is not None:
                raise ValueError("Este grafo não é ponderado; não informe peso")
            # Evita duplicação na representação direcionada
            if (u, v) not in self.arestas:
                self.arestas.append((u, v))
            if not self.direcionado and (v, u) not in self.arestas:
                self.arestas.append((v, u))
        else:
            if not isinstance(peso, (int, float)):
                raise ValueError("Peso numérico é obrigatório para grafo ponderado")
            self.arestas[(u, v)] = peso
            if not self.direcionado:
                self.arestas[(v, u)] = peso

    # -------------------- representações --------------------
    def lista_adjacencias(self, ponderada=False):
        """
        Retorna dict {v: [vizinho,...]} (não ponderada) ou {v: [(vizinho,peso),...]} (ponderada=True).
        """
        lista = {v: [] for v in self.vertices}
        if not ponderada:
            for (u, v) in self._iter_arcos():
                lista[u].append(v)
        else:
            for (u, v, w) in self._iter_arcos_pesos():
                lista[u].append((v, w))
        return lista

    def matriz_de_adjacencias(self, ponderada=False, default=0):
        """
        Não ponderada: matriz 0/1
        Ponderada: matriz de pesos (default fora da aresta)
        """
        tam = len(self.vertices)
        idx = {v: i for i, v in enumerate(self.vertices)}
        if not ponderada:
            matriz = [[0] * tam for _ in range(tam)]
            for (u, v) in self._iter_arcos():
                matriz[idx[u]][idx[v]] = 1
            return matriz
        else:
            matriz = [[default] * tam for _ in range(tam)]
            for (u, v, w) in self._iter_arcos_pesos():
                matriz[idx[u]][idx[v]] = w
            return matriz

    # -------------------- conectividade (potências da matriz) --------------------
    def conexo_por_mm(self, m=None, ignorar_indices=None):
        """
        Usa somatório de potências da matriz de adjacência (não ponderada).
        Se ponderado=True, a conectividade aqui ignora pesos (usa 0/1).
        """
        tam = len(self.vertices)
        if m is None:
            m = np.array(self.matriz_de_adjacencias(ponderada=False), dtype=int)

        R = np.zeros((tam, tam), dtype=int)

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


# -------------------- Testes rápidos --------------------
if __name__ == "__main__":
    # Teste 1 – Grafo direcionado NÃO ponderado
    # print("Teste 1: Grafo direcionado simples (não ponderado)")
    # grafo1 = Grafo(vertices=[1, 2, 3], arestas=[(1, 2), (2, 3)], direcionado=True, ponderado=False)
    # grafo1.printar_grafo()
    # print("Grau de entrada:", grafo1.grau_entrada_dos_vertices())
    # print("Grau de saída:", grafo1.grau_saida_dos_vertices())
    # print("Graus do vértice 2:", grafo1.graus_de_um_vertice(2))
    # print("Lista de adjacência:", grafo1.lista_adjacencias())
    # print("Matriz de adjacência:")
    # for linha in grafo1.matriz_de_adjacencias():
    #     print(linha)
    # print("Vértice 3 é isolado?", grafo1.vertice_isolado(3))
    # print()
    # print("Aqui!!! ",grafo1.arestas)

    # # Teste 2 – Adição de vértice e aresta (não ponderado)
    # print("Teste 2: Adicionando vértice e aresta")
    # grafo1.adicionar_vertice(4)
    # grafo1.adicionar_aresta(3, 4)
    # grafo1.printar_grafo()
    # print("Lista de adjacência atualizada:", grafo1.lista_adjacencias())
    # print()

    # Teste 3 – Grafo PONDERADO (direcionado)
    print("Teste 3: Grafo ponderado (dict)")
    grafo2 = Grafo(vertices=['A', 'B', 'C'],
                   arestas={('A', 'B'): 5, ('B', 'C'): -2},
                   direcionado=True, ponderado=True)
    
    print("aquiii !!! ", grafo2.arestas)
    grafo2.printar_grafo()
    print("Verificar aresta ('A', 'B'):", grafo2.verificar_aresta(('A', 'B')))
    print("Verificar aresta ('A', 'B', 5):", grafo2.verificar_aresta(('A', 'B', 5)))
    print("Lista de adjacência (ponderada):", grafo2.lista_adjacencias(ponderada=True))
    print("Matriz de adjacência (ponderada):")
    for linha in grafo2.matriz_de_adjacencias(ponderada=True, default=0):
        print(linha)
    print()

    # # Teste 4 – Grafo PONDERADO a partir de lista [(u,v,w)]
    # print("Teste 4: Grafo ponderado (lista)")
    # grafo3 = Grafo(vertices=[1, 2, 3],
    #                arestas=[(1, 2, 1.5), (2, 3, 0.7)],
    #                direcionado=False, ponderado=True)
    # grafo3.printar_grafo()
    # grafo3.adicionar_aresta(1, 3, peso=2.0)
    # print("Adjacências ponderadas:", grafo3.lista_adjacencias(ponderada=True))
    # print("Matriz ponderada:")
    # for linha in grafo3.matriz_de_adjacencias(ponderada=True, default=0):
    #     print(linha)

    
