import heapq
from math import inf, isfinite


LOCAIS = {
    "A": "Depósito",
    "B": "Cruzamento B",
    "C": "Cruzamento C",
    "D": "Cruzamento D",
    "E": "Cruzamento E",
    "F": "Cruzamento F",
    "G": "Cliente",
}

RUAS = (
    ("A", "B", 4), ("A", "D", 2), ("A", "E", 7),
    ("B", "C", 3), ("B", "D", 1), ("C", "D", 6),
    ("C", "G", 5), ("D", "E", 4), ("D", "F", 2),
    ("D", "G", 3), ("E", "F", 3), ("F", "G", 2),
)


def criar_grafo():
    grafo = {local: {} for local in LOCAIS}
    for origem, destino, peso in RUAS:
        grafo[origem][destino] = peso
        grafo[destino][origem] = peso
    return grafo


def alterar_rua(grafo, origem, destino, novo_peso=None, interditada=False):
    if origem not in grafo or destino not in grafo[origem]:
        raise ValueError("A rua selecionada não existe.")
    if not interditada and (
        novo_peso is None or not isfinite(novo_peso) or novo_peso < 0
    ):
        raise ValueError("A distância deve ser um número finito e não negativo.")

    # Keep the original map available for the comparison.
    copia = {local: vizinhos.copy() for local, vizinhos in grafo.items()}
    if interditada:
        del copia[origem][destino]
        del copia[destino][origem]
    else:
        copia[origem][destino] = novo_peso
        copia[destino][origem] = novo_peso
    return copia


def reconstruir_caminho(predecessores, origem, destino):
    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        if atual == origem:
            caminho.reverse()
            return caminho
        atual = predecessores.get(atual)
    return []


def dijkstra(grafo, origem, destino):
    if origem not in grafo or destino not in grafo:
        raise ValueError("Origem e destino devem pertencer ao grafo.")
    for vizinhos in grafo.values():
        for vizinho, peso in vizinhos.items():
            if vizinho not in grafo:
                raise ValueError("Há uma conexão com um vértice inexistente.")
            if not isfinite(peso) or peso < 0:
                raise ValueError("Dijkstra exige pesos finitos e não negativos.")

    distancias = {local: inf for local in grafo}
    predecessores = {local: None for local in grafo}
    distancias[origem] = 0
    fila = [(0, origem)]

    while fila:
        distancia_atual, atual = heapq.heappop(fila)
        # Older entries stay in the heap after a shorter route is found.
        if distancia_atual > distancias[atual]:
            continue
        if atual == destino:
            break

        for vizinho, peso in grafo[atual].items():
            candidata = distancia_atual + peso
            if candidata < distancias[vizinho]:
                distancias[vizinho] = candidata
                predecessores[vizinho] = atual
                heapq.heappush(fila, (candidata, vizinho))

    if distancias[destino] == inf:
        return inf, []
    return distancias[destino], reconstruir_caminho(predecessores, origem, destino)
