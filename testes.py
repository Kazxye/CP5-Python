import unittest
from math import inf

from grafo import LOCAIS, RUAS, alterar_rua, criar_grafo, dijkstra


def menor_custo_por_enumeracao(grafo, origem, destino):
    def visitar(atual, visitados, custo):
        if atual == destino:
            return custo
        return min(
            (visitar(vizinho, visitados | {vizinho}, custo + peso)
             for vizinho, peso in grafo[atual].items() if vizinho not in visitados),
            default=inf,
        )
    return visitar(origem, {origem}, 0)


class TestesRotas(unittest.TestCase):
    def setUp(self):
        self.grafo = criar_grafo()

    def test_dados_do_enunciado(self):
        self.assertEqual(set(self.grafo), set(LOCAIS))
        self.assertEqual(sum(map(len, self.grafo.values())), 24)
        for origem, destino, peso in RUAS:
            self.assertEqual(self.grafo[origem][destino], peso)
            self.assertEqual(self.grafo[destino][origem], peso)

    def test_casos_obrigatorios(self):
        casos = [
            ("A", "G", 5, ["A", "D", "G"]),
            ("A", "C", 6, ["A", "D", "B", "C"]),
            ("E", "C", 8, ["E", "D", "B", "C"]),
            ("G", "A", 5, ["G", "D", "A"]),
        ]
        for origem, destino, distancia, caminho in casos:
            with self.subTest(origem=origem, destino=destino):
                self.assertEqual(dijkstra(self.grafo, origem, destino), (distancia, caminho))
                print(f"{origem} -> {destino}: {' -> '.join(caminho)} | {distancia} km")

    def test_todos_os_pares_contra_enumeracao(self):
        # Exhaustive search is feasible here because the map has only 7 vertices.
        for origem in self.grafo:
            for destino in self.grafo:
                with self.subTest(origem=origem, destino=destino):
                    distancia, caminho = dijkstra(self.grafo, origem, destino)
                    self.assertEqual(distancia, menor_custo_por_enumeracao(self.grafo, origem, destino))
                    self.assertEqual(caminho[0], origem)
                    self.assertEqual(caminho[-1], destino)
                    self.assertEqual(sum(self.grafo[a][b] for a, b in zip(caminho, caminho[1:])), distancia)

    def test_mesmo_ponto(self):
        self.assertEqual(dijkstra(self.grafo, "A", "A"), (0, ["A"]))

    def test_destino_sem_conexao(self):
        self.assertEqual(dijkstra({"A": {}, "G": {}}, "A", "G"), (inf, []))

    def test_entradas_invalidas(self):
        with self.assertRaises(ValueError):
            dijkstra(self.grafo, "X", "G")
        for peso in (-1, float("nan"), inf):
            with self.subTest(peso=peso), self.assertRaises(ValueError):
                dijkstra({"A": {"G": peso}, "G": {"A": peso}}, "A", "G")
        with self.assertRaises(ValueError):
            dijkstra({"A": {"X": 1}, "G": {}}, "A", "G")

    def test_interdicao(self):
        cenario = alterar_rua(self.grafo, "D", "G", interditada=True)
        self.assertNotIn("G", cenario["D"])
        self.assertNotIn("D", cenario["G"])
        self.assertEqual(dijkstra(cenario, "A", "G"), (6, ["A", "D", "F", "G"]))
        self.assertEqual(self.grafo["D"]["G"], 3)

    def test_alteracao_de_distancia(self):
        cenario = alterar_rua(self.grafo, "D", "G", novo_peso=10)
        self.assertEqual(cenario["G"]["D"], 10)
        self.assertEqual(dijkstra(cenario, "A", "G"), (6, ["A", "D", "F", "G"]))
        self.assertEqual(self.grafo["D"]["G"], 3)
        self.assertEqual(dijkstra(alterar_rua(self.grafo, "D", "G", 0), "A", "G"), (2, ["A", "D", "G"]))

    def test_alteracao_invalida(self):
        with self.assertRaises(ValueError):
            alterar_rua(self.grafo, "A", "G", novo_peso=1)
        for peso in (None, -2, inf, float("nan")):
            with self.subTest(peso=peso), self.assertRaises(ValueError):
                alterar_rua(self.grafo, "D", "G", novo_peso=peso)


if __name__ == "__main__":
    unittest.main(verbosity=2)
