"""Benchmarks sinteticos dos algoritmos."""

import random
import time
import tracemalloc
from typing import Callable

from src.algorithms import dijkstra, guloso
from src.graph import Grafo, gerar_grafo_completo_direcionado

LinhaBenchmark = dict[str, float]
Algoritmo = Callable[[Grafo, int, list[int]], tuple[dict[int, float], dict[int, list[int]], int]]


def executar_benchmark_algoritmo(
    nome: str,
    algoritmo: Algoritmo,
    maximo_vertices: int = 30,
) -> list[LinhaBenchmark]:
    """Executa um algoritmo em grafos completos de 4 ate maximo_vertices."""
    if maximo_vertices < 4:
        raise ValueError("N deve ser pelo menos 4 para executar o benchmark.")

    resultados: list[LinhaBenchmark] = []
    aleatorio = random.Random(42)

    for quantidade_vertices in range(4, maximo_vertices + 1):
        print(f"[INFO] Benchmark {nome}: {quantidade_vertices} vertices...")
        grafo = gerar_grafo_completo_direcionado(
            quantidade_vertices,
            semente=quantidade_vertices,
        )
        origem = aleatorio.randint(0, quantidade_vertices - 1)
        destinos = [
            vertice for vertice in range(quantidade_vertices) if vertice != origem
        ]

        # Medicoes usadas no relatorio: comparacoes, tempo e memoria de pico.
        tracemalloc.start()
        inicio = time.perf_counter()
        _, _, comparacoes = algoritmo(grafo, origem, destinos)
        tempo = time.perf_counter() - inicio
        _, pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        resultados.append(
            {
                "vertices": quantidade_vertices,
                "comparacoes": comparacoes,
                "tempo_segundos": tempo,
                "memoria_kb": pico / 1024,
                "origem": origem,
            }
        )

    return resultados


def executar_benchmark_dijkstra(maximo_vertices: int = 30) -> list[LinhaBenchmark]:
    """Executa o benchmark do Dijkstra."""
    return executar_benchmark_algoritmo("Dijkstra", dijkstra, maximo_vertices)


def executar_benchmark_guloso(maximo_vertices: int = 30) -> list[LinhaBenchmark]:
    """Executa o benchmark da heuristica gulosa."""
    return executar_benchmark_algoritmo("Guloso", guloso, maximo_vertices)


# Aliases mantidos para compatibilidade.
BenchmarkRow = LinhaBenchmark
Algorithm = Algoritmo
run_algorithm_benchmark = executar_benchmark_algoritmo
run_dijkstra_benchmark = executar_benchmark_dijkstra
run_greedy_benchmark = executar_benchmark_guloso
