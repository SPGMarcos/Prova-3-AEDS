"""Funcoes basicas para grafos direcionados ponderados."""

import random
from typing import Iterable, Optional

Vertice = int
Peso = float
Aresta = tuple[Vertice, Peso]
Grafo = dict[Vertice, list[Aresta]]

# Aliases em ingles para nao quebrar imports antigos.
Vertex = Vertice
Weight = Peso
Edge = Aresta
Graph = Grafo


def adicionar_aresta(
    grafo: Grafo,
    origem: Vertice,
    destino: Vertice,
    peso: Peso,
) -> None:
    """Adiciona uma aresta direcionada com peso positivo."""
    if peso <= 0:
        raise ValueError("Todos os pesos do grafo devem ser positivos.")

    grafo.setdefault(origem, [])
    grafo.setdefault(destino, [])
    grafo[origem].append((destino, peso))


def construir_grafo(arestas: Iterable[tuple[Vertice, Vertice, Peso]]) -> Grafo:
    """Constroi um grafo a partir de arestas no formato origem, destino e peso."""
    grafo: Grafo = {}
    for origem, destino, peso in arestas:
        adicionar_aresta(grafo, origem, destino, peso)
    return grafo


def contar_arestas(grafo: Grafo) -> int:
    """Conta o total de arestas do grafo."""
    return sum(len(vizinhos) for vizinhos in grafo.values())


def ultimo_vertice(grafo: Grafo) -> Vertice:
    """Retorna o maior identificador de vertice."""
    if not grafo:
        raise ValueError("Grafo vazio: nao ha ultimo vertice.")
    return max(grafo)


def gerar_grafo_completo_direcionado(
    quantidade_vertices: int,
    peso_minimo: int = 1,
    peso_maximo: int = 100,
    semente: Optional[int] = None,
) -> Grafo:
    """Gera um grafo completo direcionado com pesos aleatorios."""
    if quantidade_vertices < 2:
        raise ValueError("O grafo deve possuir pelo menos 2 vertices.")

    aleatorio = random.Random(semente) if semente is not None else random
    grafo: Grafo = {vertice: [] for vertice in range(quantidade_vertices)}

    for origem in range(quantidade_vertices):
        for destino in range(quantidade_vertices):
            if origem != destino:
                adicionar_aresta(
                    grafo,
                    origem,
                    destino,
                    aleatorio.randint(peso_minimo, peso_maximo),
                )

    return grafo


# Aliases mantidos para compatibilidade.
add_edge = adicionar_aresta
build_graph = construir_grafo
edge_count = contar_arestas
last_vertex = ultimo_vertice
generate_complete_directed_graph = gerar_grafo_completo_direcionado
