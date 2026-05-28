"""Algoritmos de caminho minimo e contagem de comparacoes."""

import heapq
from dataclasses import dataclass
from typing import Iterable, Optional

from src.graph import Grafo, Peso, Vertice


@dataclass
class ContadorComparacoes:
    """Contador simples usado nos algoritmos."""

    total: int = 0

    def incrementar(self, quantidade: int = 1) -> None:
        """Incrementa a contagem."""
        if quantidade < 0:
            raise ValueError("O incremento nao pode ser negativo.")
        self.total += quantidade


def _reconstruir_caminho(
    anteriores: dict[Vertice, Optional[Vertice]],
    origem: Vertice,
    destino: Vertice,
) -> list[Vertice]:
    """Reconstrui um caminho a partir dos predecessores."""
    if destino not in anteriores:
        return []

    caminho: list[Vertice] = []
    atual: Optional[Vertice] = destino
    while atual is not None:
        caminho.append(atual)
        if atual == origem:
            break
        atual = anteriores.get(atual)

    caminho.reverse()
    return caminho if caminho and caminho[0] == origem else []


def dijkstra(
    grafo: Grafo,
    origem: Vertice,
    destinos: Optional[Iterable[Vertice]] = None,
) -> tuple[dict[Vertice, Peso], dict[Vertice, list[Vertice]], int]:
    """Calcula caminhos minimos de uma origem para um ou mais destinos."""
    if origem not in grafo:
        raise ValueError("A origem informada nao existe no grafo.")

    contador = ContadorComparacoes()
    alvos = set(destinos) if destinos is not None else None
    alvos_restantes = set(alvos) if alvos is not None else None

    distancias: dict[Vertice, Peso] = {origem: 0}
    anteriores: dict[Vertice, Optional[Vertice]] = {origem: None}
    visitados: set[Vertice] = set()
    fila: list[tuple[Peso, Vertice]] = [(0, origem)]

    # O vertice retirado da fila sempre e o de menor distancia conhecida.
    while fila:
        distancia_atual, vertice_atual = heapq.heappop(fila)

        contador.incrementar()
        if vertice_atual in visitados:
            continue

        contador.incrementar()
        if distancia_atual > distancias.get(vertice_atual, float("inf")):
            continue

        visitados.add(vertice_atual)

        if alvos_restantes is not None and vertice_atual in alvos_restantes:
            alvos_restantes.remove(vertice_atual)
            contador.incrementar()
            if not alvos_restantes:
                break

        for vizinho, peso in grafo.get(vertice_atual, []):
            contador.incrementar()
            if vizinho in visitados:
                continue

            nova_distancia = distancia_atual + peso
            distancia_antiga = distancias.get(vizinho, float("inf"))

            contador.incrementar()
            if nova_distancia < distancia_antiga:
                distancias[vizinho] = nova_distancia
                anteriores[vizinho] = vertice_atual
                heapq.heappush(fila, (nova_distancia, vizinho))

    vertices_retorno = distancias.keys() if alvos is None else alvos
    distancias_retorno = {
        destino: distancias.get(destino, float("inf"))
        for destino in vertices_retorno
    }
    caminhos = {
        destino: _reconstruir_caminho(anteriores, origem, destino)
        for destino in vertices_retorno
    }

    return distancias_retorno, caminhos, contador.total


def caminho_guloso_para_destino(
    grafo: Grafo,
    origem: Vertice,
    destino: Vertice,
) -> tuple[list[Vertice], Peso, int]:
    """Monta um caminho escolhendo sempre a menor aresta local."""
    if origem not in grafo:
        raise ValueError("A origem informada nao existe no grafo.")

    contador = ContadorComparacoes()
    atual = origem
    visitados: set[Vertice] = {origem}
    caminho: list[Vertice] = [origem]
    custo_total: Peso = 0

    # A escolha local e simples, mas nao garante o menor caminho global.
    while atual != destino:
        melhor_vizinho: Optional[Vertice] = None
        melhor_peso: Peso = float("inf")

        for vizinho, peso in grafo.get(atual, []):
            contador.incrementar()
            if vizinho in visitados:
                continue

            contador.incrementar()
            if peso < melhor_peso:
                melhor_vizinho = vizinho
                melhor_peso = peso

        contador.incrementar()
        if melhor_vizinho is None:
            return [], float("inf"), contador.total

        atual = melhor_vizinho
        visitados.add(atual)
        caminho.append(atual)
        custo_total += melhor_peso

    return caminho, custo_total, contador.total


def guloso(
    grafo: Grafo,
    origem: Vertice,
    destinos: Iterable[Vertice],
) -> tuple[dict[Vertice, Peso], dict[Vertice, list[Vertice]], int]:
    """Executa a heuristica gulosa para varios destinos."""
    distancias: dict[Vertice, Peso] = {}
    caminhos: dict[Vertice, list[Vertice]] = {}
    total_comparacoes = 0

    for destino in destinos:
        caminho, custo, comparacoes = caminho_guloso_para_destino(grafo, origem, destino)
        caminhos[destino] = caminho
        distancias[destino] = custo
        total_comparacoes += comparacoes

    return distancias, caminhos, total_comparacoes


# Alias mantido para compatibilidade com qualquer chamada antiga.
greedy = guloso
