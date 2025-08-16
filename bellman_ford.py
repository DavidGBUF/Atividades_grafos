from grafo_utils import Grafo

def bellman_ford(grafo: Grafo, origem):
    dist = {v: float("inf") for v in grafo.vertices}
    pai = {v: None for v in grafo.vertices}
    dist[origem] = 0

    if grafo.ponderado:
        arestas = [(u, v, w) for (u, v), w in grafo.arestas.items()]
    else:
        arestas = [(u, v, 1) for (u, v) in grafo.arestas]

    for _ in range(len(grafo.vertices) - 1):
        atualizado = False
        for (u, v, w) in arestas:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pai[v] = u
                atualizado = True
        if not atualizado:
            break

    for (u, v, w) in arestas:
        if dist[u] + w < dist[v]:
            raise ValueError("Ciclo de peso negativo detectado!")

    return dist, pai


g = Grafo(
    vertices=["A", "B", "C", "D", "E"],
    arestas=[
        ("A", "B", 6),
        ("A", "D", 7),
        ("B", "C", 5),
        ("B", "D", 8),
        ("B", "E", -4),
        ("C", "B", -2),
        ("D", "C", -3),
        ("D", "E", 9),
        ("E", "A", 2),
        ("E", "C", 7),
    ],
    direcionado=True,
    ponderado=True,
)

dist, pai = bellman_ford(g, "A")

print("Distâncias mínimas:", dist)
print("Predecessores:", pai)
